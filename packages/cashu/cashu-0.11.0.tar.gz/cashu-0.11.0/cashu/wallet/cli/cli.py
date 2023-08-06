#!/usr/bin/env python

import asyncio
import base64
import json
import os
import sys
import time
from datetime import datetime
from functools import wraps
from itertools import groupby, islice
from operator import itemgetter
from os import listdir
from os.path import isdir, join
from typing import Dict, List

import click
from click import Context
from loguru import logger

from cashu.core.base import Proof, TokenV1, TokenV2
from cashu.core.helpers import sum_proofs
from cashu.core.migrations import migrate_databases
from cashu.core.settings import settings
from cashu.nostr.nostr.client.client import NostrClient
from cashu.tor.tor import TorProxy
from cashu.wallet import migrations
from cashu.wallet.crud import (
    get_keyset,
    get_lightning_invoices,
    get_reserved_proofs,
    get_unused_locks,
)
from cashu.wallet.wallet import Wallet as Wallet

from .cli_helpers import (
    get_mint_wallet,
    print_mint_balances,
    redeem_TokenV3_multimint,
    serialize_TokenV1_to_TokenV3,
    serialize_TokenV2_to_TokenV3,
)
from .nostr import receive_nostr, send_nostr


async def init_wallet(wallet: Wallet):
    """Performs migrations and loads proofs from db."""
    await migrate_databases(wallet.db, migrations)
    await wallet.load_proofs()


class NaturalOrderGroup(click.Group):
    """For listing commands in help in order of definition"""

    def list_commands(self, ctx):
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
@click.option(
    "--host",
    "-h",
    default=settings.mint_url,
    help=f"Mint URL (default: {settings.mint_url}).",
)
@click.option(
    "--wallet",
    "-w",
    "walletname",
    default="wallet",
    help="Wallet name (default: wallet).",
)
@click.pass_context
def cli(ctx: Context, host: str, walletname: str):
    if settings.tor and not TorProxy().check_platform():
        error_str = "Your settings say TOR=true but the built-in Tor bundle is not supported on your system. You have two options: Either install Tor manually and set TOR=FALSE and SOCKS_HOST=localhost and SOCKS_PORT=9050 in your Cashu config (recommended). Or turn off Tor by setting TOR=false (not recommended). Cashu will not work until you edit your config file accordingly."
        error_str += "\n\n"
        if settings.env_file:
            error_str += f"Edit your Cashu config file here: {settings.env_file}"
            env_path = settings.env_file
        else:
            error_str += f"Ceate a new Cashu config file here: {os.path.join(settings.cashu_dir, '.env')}"
            env_path = os.path.join(settings.cashu_dir, ".env")
        error_str += f'\n\nYou can turn off Tor with this command: echo "TOR=FALSE" >> {env_path}'
        raise Exception(error_str)

    ctx.ensure_object(dict)
    ctx.obj["HOST"] = host
    ctx.obj["WALLET_NAME"] = walletname
    wallet = Wallet(ctx.obj["HOST"], os.path.join(settings.cashu_dir, walletname))
    ctx.obj["WALLET"] = wallet
    asyncio.run(init_wallet(wallet))
    pass


# https://github.com/pallets/click/issues/85#issuecomment-503464628
def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@cli.command("pay", help="Pay Lightning invoice.")
@click.argument("invoice", type=str)
@click.option(
    "--yes", "-y", default=False, is_flag=True, help="Skip confirmation.", type=bool
)
@click.pass_context
@coro
async def pay(ctx: Context, invoice: str, yes: bool):
    wallet: Wallet = ctx.obj["WALLET"]
    await wallet.load_mint()
    wallet.status()
    total_amount, fee_reserve_sat = await wallet.get_pay_amount_with_fees(invoice)
    if not yes:
        click.confirm(
            f"Pay {total_amount - fee_reserve_sat} sat ({total_amount} sat with potential fees)?",
            abort=True,
            default=True,
        )

    print(f"Paying Lightning invoice ...")
    assert total_amount > 0, "amount is not positive"
    if wallet.available_balance < total_amount:
        print("Error: Balance too low.")
        return
    _, send_proofs = await wallet.split_to_send(wallet.proofs, total_amount)  # type: ignore
    await wallet.pay_lightning(send_proofs, invoice)
    await wallet.load_proofs()
    wallet.status()


@cli.command("invoice", help="Create Lighting invoice.")
@click.argument("amount", type=int)
@click.option("--hash", default="", help="Hash of the paid invoice.", type=str)
@click.pass_context
@coro
async def invoice(ctx: Context, amount: int, hash: str):
    wallet: Wallet = ctx.obj["WALLET"]
    await wallet.load_mint()
    wallet.status()
    if not settings.lightning:
        r = await wallet.mint(amount)
    elif amount and not hash:
        invoice = await wallet.request_mint(amount)
        if invoice.pr:
            print(f"Pay invoice to mint {amount} sat:")
            print("")
            print(f"Invoice: {invoice.pr}")
            print("")
            print(
                f"If you abort this you can use this command to recheck the invoice:\ncashu invoice {amount} --hash {invoice.hash}"
            )
            check_until = time.time() + 5 * 60  # check for five minutes
            print("")
            print(
                f"Checking invoice ...",
                end="",
                flush=True,
            )
            paid = False
            while time.time() < check_until and not paid:
                time.sleep(3)
                try:
                    await wallet.mint(amount, invoice.hash)
                    paid = True
                    print(" Invoice paid.")
                except Exception as e:
                    # TODO: user error codes!
                    if str(e) == "Error: Lightning invoice not paid yet.":
                        print(".", end="", flush=True)
                        continue
            if not paid:
                print("\n")
                print(
                    "Invoice is not paid yet, stopping check. Use the command above to recheck after the invoice has been paid."
                )
    elif amount and hash:
        await wallet.mint(amount, hash)
    wallet.status()
    return


@cli.command("balance", help="Balance.")
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    help="Show pending tokens as well.",
    type=bool,
)
@click.pass_context
@coro
async def balance(ctx: Context, verbose):
    wallet: Wallet = ctx.obj["WALLET"]
    if verbose:
        # show balances per keyset
        keyset_balances = wallet.balance_per_keyset()
        if len(keyset_balances) > 1:
            print(f"You have balances in {len(keyset_balances)} keysets:")
            print("")
            for k, v in keyset_balances.items():
                print(
                    f"Keyset: {k} - Balance: {v['available']} sat (pending: {v['balance']-v['available']} sat)"
                )
            print("")

    await print_mint_balances(ctx, wallet)

    if verbose:
        print(
            f"Balance: {wallet.available_balance} sat (pending: {wallet.balance-wallet.available_balance} sat) in {len([p for p in wallet.proofs if not p.reserved])} tokens"
        )
    else:
        print(f"Balance: {wallet.available_balance} sat")


async def send(ctx: Context, amount: int, lock: str, legacy: bool):
    """
    Prints token to send to stdout.
    """
    if lock and len(lock) < 22:
        print("Error: lock has to be at least 22 characters long.")
        return
    p2sh = False
    if lock and len(lock.split("P2SH:")) == 2:
        p2sh = True

    wallet = await get_mint_wallet(ctx)
    await wallet.load_proofs()

    _, send_proofs = await wallet.split_to_send(
        wallet.proofs, amount, lock, set_reserved=True
    )
    token = await wallet.serialize_proofs(
        send_proofs,
        include_mints=True,
    )
    print(token)

    if legacy:
        print("")
        print("Old token format:")
        print("")
        token = await wallet.serialize_proofs(
            send_proofs,
            legacy=True,
        )
        print(token)

    wallet.status()


@cli.command("send", help="Send tokens.")
@click.argument("amount", type=int)
@click.argument("nostr", type=str, required=False)
@click.option(
    "--nostr",
    "-n",
    "nopt",
    help="Send to nostr pubkey.",
    type=str,
)
@click.option("--lock", "-l", default=None, help="Lock tokens (P2SH).", type=str)
@click.option(
    "--legacy",
    "-l",
    default=False,
    is_flag=True,
    help="Print legacy token without mint information.",
    type=bool,
)
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    help="Show more information.",
    type=bool,
)
@click.option(
    "--yes", "-y", default=False, is_flag=True, help="Skip confirmation.", type=bool
)
@click.pass_context
@coro
async def send_command(
    ctx,
    amount: int,
    nostr: str,
    nopt: str,
    lock: str,
    legacy: bool,
    verbose: bool,
    yes: bool,
):
    if not nostr and not nopt:
        await send(ctx, amount, lock, legacy)
    else:
        await send_nostr(ctx, amount, nostr or nopt, verbose, yes)


async def receive(ctx: Context, token: str, lock: str):
    wallet: Wallet = ctx.obj["WALLET"]
    # await wallet.load_mint()

    # check for P2SH locks
    if lock:
        # load the script and signature of this address from the database
        assert len(lock.split("P2SH:")) == 2, Exception(
            "lock has wrong format. Expected P2SH:<address>."
        )
        address_split = lock.split("P2SH:")[1]
        p2shscripts = await get_unused_locks(address_split, db=wallet.db)
        assert len(p2shscripts) == 1, Exception("lock not found.")
        script, signature = p2shscripts[0].script, p2shscripts[0].signature
    else:
        script, signature = None, None

    # deserialize token

    # ----- backwards compatibility -----

    # V2Tokens (0.7-0.11.0) (eyJwcm9...)
    if token.startswith("eyJwcm9"):
        try:
            tokenv2 = TokenV2.parse_obj(json.loads(base64.urlsafe_b64decode(token)))
            token = await serialize_TokenV2_to_TokenV3(wallet, tokenv2)
        except:
            pass

    # V1Tokens (<0.7) (W3siaWQ...)
    if token.startswith("W3siaWQ"):
        try:
            tokenv1 = TokenV1.parse_obj(json.loads(base64.urlsafe_b64decode(token)))
            token = await serialize_TokenV1_to_TokenV3(wallet, tokenv1)
            print(token)
        except:
            pass
    # ----- receive token -----

    # deserialize token
    # dtoken = json.loads(base64.urlsafe_b64decode(token))
    tokenObj = wallet._deserialize_token_V3(token)

    # tokenObj = TokenV2.parse_obj(dtoken)
    assert len(tokenObj.token), Exception("no proofs in token")
    assert len(tokenObj.token[0].proofs), Exception("no proofs in token")
    includes_mint_info: bool = any([t.mint for t in tokenObj.token])

    # if there is a `mints` field in the token
    # we check whether the token has mints that we don't know yet
    # and ask the user if they want to trust the new mitns
    if includes_mint_info:
        # we ask the user to confirm any new mints the tokens may include
        # await verify_mints(ctx, tokenObj)
        # redeem tokens with new wallet instances
        await redeem_TokenV3_multimint(ctx, tokenObj, script, signature)
    else:
        # no mint information present, we extract the proofs and use wallet's default mint

        proofs = [p for t in tokenObj.token for p in t.proofs]
        # first we load the mint URL from the DB
        keyset_in_token = proofs[0].id
        assert keyset_in_token
        # we get the keyset from the db
        mint_keysets = await get_keyset(id=keyset_in_token, db=wallet.db)
        assert mint_keysets, Exception("we don't know this keyset")
        assert mint_keysets.mint_url, Exception("we don't know this mint's URL")
        # now we have the URL
        mint_wallet = Wallet(
            mint_keysets.mint_url,
            os.path.join(settings.cashu_dir, ctx.obj["WALLET_NAME"]),
        )
        await mint_wallet.load_mint(keyset_in_token)
        _, _ = await mint_wallet.redeem(proofs, script, signature)
        print(f"Received {sum_proofs(proofs)} sats")

    # reload main wallet so the balance updates
    await wallet.load_proofs()
    wallet.status()


@cli.command("receive", help="Receive tokens.")
@click.argument("token", type=str, default="")
@click.option("--lock", "-l", default=None, help="Unlock tokens.", type=str)
@click.option(
    "--nostr", "-n", default=False, is_flag=True, help="Receive tokens via nostr."
)
@click.option(
    "--all", "-a", default=False, is_flag=True, help="Receive all pending tokens."
)
@click.option(
    "--verbose",
    "-v",
    help="Display more information.",
    is_flag=True,
    default=False,
    type=bool,
)
@click.pass_context
@coro
async def receive_cli(
    ctx: Context, token: str, lock: str, nostr: bool, all: bool, verbose: bool
):
    wallet: Wallet = ctx.obj["WALLET"]
    wallet.status()
    if token:
        await receive(ctx, token, lock)
    elif nostr:
        await receive_nostr(ctx, verbose)
    elif all:
        reserved_proofs = await get_reserved_proofs(wallet.db)
        if len(reserved_proofs):
            for (key, value) in groupby(reserved_proofs, key=itemgetter("send_id")):  # type: ignore
                proofs = list(value)
                token = await wallet.serialize_proofs(proofs)
                await receive(ctx, token, lock)
    else:
        print("Error: enter token or use either flag --nostr or --all.")


@cli.command("burn", help="Burn spent tokens.")
@click.argument("token", required=False, type=str)
@click.option("--all", "-a", default=False, is_flag=True, help="Burn all spent tokens.")
@click.option(
    "--delete",
    "-d",
    default=None,
    help="Forcefully delete pending token by send ID if mint is unavailable.",
)
@click.option(
    "--force", "-f", default=False, is_flag=True, help="Force check on all tokens."
)
@click.pass_context
@coro
async def burn(ctx: Context, token: str, all: bool, force: bool, delete: str):
    wallet: Wallet = ctx.obj["WALLET"]
    if not delete:
        await wallet.load_mint()
    if not (all or token or force or delete) or (token and all):
        print(
            "Error: enter a token or use --all to burn all pending tokens, --force to check all tokens or"
            "or --delete with send ID to force-delete pending token from list if mint is unavailable."
        )
        return
    if all:
        # check only those who are flagged as reserved
        proofs = await get_reserved_proofs(wallet.db)
    elif force:
        # check all proofs in db
        proofs = wallet.proofs
    elif delete:
        reserved_proofs = await get_reserved_proofs(wallet.db)
        proofs = [proof for proof in reserved_proofs if proof["send_id"] == delete]
    else:
        # check only the specified ones
        proofs = [Proof(**p) for p in json.loads(base64.urlsafe_b64decode(token))]

    if delete:
        await wallet.invalidate(proofs, check_spendable=False)
    else:
        await wallet.invalidate(proofs)
    wallet.status()


@cli.command("pending", help="Show pending tokens.")
@click.option(
    "--legacy",
    "-l",
    default=False,
    is_flag=True,
    help="Print legacy token without mint information.",
    type=bool,
)
@click.option(
    "--number", "-n", default=None, help="Show only n pending tokens.", type=int
)
@click.option(
    "--offset",
    default=0,
    help="Show pending tokens only starting from offset.",
    type=int,
)
@click.pass_context
@coro
async def pending(ctx: Context, legacy, number: int, offset: int):
    wallet: Wallet = ctx.obj["WALLET"]
    reserved_proofs = await get_reserved_proofs(wallet.db)
    if len(reserved_proofs):
        print(f"--------------------------\n")
        sorted_proofs = sorted(reserved_proofs, key=itemgetter("send_id"))  # type: ignore
        if number:
            number += offset
        for i, (key, value) in islice(
            enumerate(
                groupby(
                    sorted_proofs,
                    key=itemgetter("send_id"),
                )
            ),
            offset,
            number,
        ):
            grouped_proofs = list(value)
            token = await wallet.serialize_proofs(grouped_proofs)
            # token_hidden_secret = await wallet.serialize_proofs(grouped_proofs)
            reserved_date = datetime.utcfromtimestamp(
                int(grouped_proofs[0].time_reserved)
            ).strftime("%Y-%m-%d %H:%M:%S")
            print(
                f"#{i} Amount: {sum_proofs(grouped_proofs)} sat Time: {reserved_date} ID: {key}\n"
            )
            print(f"{token}\n")

            if legacy:
                token_legacy = await wallet.serialize_proofs(
                    grouped_proofs,
                    legacy=True,
                )
                print(f"{token_legacy}\n")
            print(f"--------------------------\n")
        print("To remove all spent tokens use: cashu burn -a")


@cli.command("lock", help="Generate receiving lock.")
@click.pass_context
@coro
async def lock(ctx):
    wallet: Wallet = ctx.obj["WALLET"]
    p2shscript = await wallet.create_p2sh_lock()
    txin_p2sh_address = p2shscript.address
    print("---- Pay to script hash (P2SH) ----\n")
    print("Use a lock to receive tokens that only you can unlock.")
    print("")
    print(f"Public receiving lock: P2SH:{txin_p2sh_address}")
    print("")
    print(
        f"Anyone can send tokens to this lock:\n\ncashu send <amount> --lock P2SH:{txin_p2sh_address}"
    )
    print("")
    print(
        f"Only you can receive tokens from this lock:\n\ncashu receive <token> --lock P2SH:{txin_p2sh_address}\n"
    )


@cli.command("locks", help="Show unused receiving locks.")
@click.pass_context
@coro
async def locks(ctx):
    wallet: Wallet = ctx.obj["WALLET"]
    locks = await get_unused_locks(db=wallet.db)
    if len(locks):
        print("")
        print(f"--------------------------\n")
        for l in locks:
            print(f"Address: {l.address}")
            print(f"Script: {l.script}")
            print(f"Signature: {l.signature}")
            print("")
            print(f"Receive: cashu receive <token> --lock P2SH:{l.address}")
            print("")
            print(f"--------------------------\n")
    else:
        print("No locks found. Create one using: cashu lock")
    return True


@cli.command("invoices", help="List of all pending invoices.")
@click.pass_context
@coro
async def invoices(ctx):
    wallet: Wallet = ctx.obj["WALLET"]
    invoices = await get_lightning_invoices(db=wallet.db)
    if len(invoices):
        print("")
        print(f"--------------------------\n")
        for invoice in invoices:
            print(f"Paid: {invoice.paid}")
            print(f"Incoming: {invoice.amount > 0}")
            print(f"Amount: {abs(invoice.amount)}")
            if invoice.hash:
                print(f"Hash: {invoice.hash}")
            if invoice.preimage:
                print(f"Preimage: {invoice.preimage}")
            if invoice.time_created:
                d = datetime.utcfromtimestamp(
                    int(float(invoice.time_created))
                ).strftime("%Y-%m-%d %H:%M:%S")
                print(f"Created: {d}")
            if invoice.time_paid:
                d = datetime.utcfromtimestamp(int(float(invoice.time_paid))).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                print(f"Paid: {d}")
            print("")
            print(f"Payment request: {invoice.pr}")
            print("")
            print(f"--------------------------\n")
    else:
        print("No invoices found.")


@cli.command("wallets", help="List of all available wallets.")
@click.pass_context
@coro
async def wallets(ctx):
    # list all directories
    wallets = [
        d for d in listdir(settings.cashu_dir) if isdir(join(settings.cashu_dir, d))
    ]
    try:
        wallets.remove("mint")
    except ValueError:
        pass
    for w in wallets:
        wallet = Wallet(ctx.obj["HOST"], os.path.join(settings.cashu_dir, w))
        try:
            await init_wallet(wallet)
            if wallet.proofs and len(wallet.proofs):
                active_wallet = False
                if w == ctx.obj["WALLET_NAME"]:
                    active_wallet = True
                print(
                    f"Wallet: {w}\tBalance: {sum_proofs(wallet.proofs)} sat (available: {sum_proofs([p for p in wallet.proofs if not p.reserved])} sat){' *' if active_wallet else ''}"
                )
        except:
            pass


@cli.command("info", help="Information about Cashu wallet.")
@click.pass_context
@coro
async def info(ctx: Context):
    print(f"Version: {settings.version}")
    print(f"Wallet: {ctx.obj['WALLET_NAME']}")
    if settings.debug:
        print(f"Debug: {settings.debug}")
    print(f"Cashu dir: {settings.cashu_dir}")
    if settings.env_file:
        print(f"Settings: {settings.env_file}")
    if settings.tor:
        print(f"Tor enabled: {settings.tor}")
    if settings.nostr_private_key:
        try:
            client = NostrClient(private_key=settings.nostr_private_key, connect=False)
            print(f"Nostr public key: {client.public_key.bech32()}")
            print(f"Nostr relays: {settings.nostr_relays}")
        except:
            print(f"Nostr: Error. Invalid key.")
    if settings.socks_host:
        print(f"Socks proxy: {settings.socks_host}:{settings.socks_port}")
    print(f"Mint URL: {ctx.obj['HOST']}")
    return
