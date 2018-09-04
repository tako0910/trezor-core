from trezor import log, ui, wire
from trezor.crypto import bip32
from trezor.crypto.curve import ed25519
from trezor.messages.CardanoMessageSignature import CardanoMessageSignature

from .address import derive_address_and_node, validate_full_path
from .layout import confirm_with_pagination

from apps.common import paths, seed, storage


async def sign_message(ctx, msg):
    await paths.validate_path(ctx, validate_full_path, path=msg.address_n)

    mnemonic = storage.get_mnemonic()
    root_node = bip32.from_mnemonic_cardano(mnemonic)

    try:
        signature = _sign_message(root_node, msg.message, msg.address_n)
    except ValueError as e:
        if __debug__:
            log.exception(__name__, e)
        raise wire.ProcessError("Signing failed")
    mnemonic = None
    root_node = None

    if not await confirm_with_pagination(
        ctx, msg.message, "Signing message", ui.ICON_RECEIVE, ui.GREEN
    ):
        raise wire.ActionCancelled("Signing cancelled")

    if not await confirm_with_pagination(
        ctx,
        paths.break_address_n_to_lines(msg.address_n),
        "With address",
        ui.ICON_RECEIVE,
        ui.GREEN,
    ):
        raise wire.ActionCancelled("Signing cancelled")

    return signature


def _sign_message(root_node, message: str, derivation_path: list):
    address, node = derive_address_and_node(root_node, derivation_path)

    signature = ed25519.sign_ext(node.private_key(), node.private_key_ext(), message)

    sig = CardanoMessageSignature()
    sig.public_key = seed.remove_ed25519_prefix(node.public_key())
    sig.signature = signature

    return sig
