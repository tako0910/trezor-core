from trezor import ui, wire
from trezor.messages.MessageType import TxAck
from trezor.messages.RequestType import TXFINISHED
from trezor.messages.TxRequest import TxRequest

from apps.common import coins, paths, seed
from apps.wallet.sign_tx.helpers import (
    UiConfirmFeeOverThreshold,
    UiConfirmForeignAddress,
    UiConfirmOutput,
    UiConfirmTotal,
)


@ui.layout
async def sign_tx(ctx, msg):
    from apps.wallet.sign_tx import layout, progress, signing

    coin_name = msg.coin_name or "Bitcoin"
    coin = coins.by_name(coin_name)
    # TODO: rework this so we don't have to pass root to signing.sign_tx
    root = await seed.derive_node(ctx, [], curve_name=coin.curve_name)

    signer = signing.sign_tx(msg, root)
    res = None
    while True:
        try:
            req = signer.send(res)
        except signing.SigningError as e:
            raise wire.Error(*e.args)
        except signing.MultisigError as e:
            raise wire.Error(*e.args)
        except signing.AddressError as e:
            raise wire.Error(*e.args)
        except signing.ScriptsError as e:
            raise wire.Error(*e.args)
        except signing.Bip143Error as e:
            raise wire.Error(*e.args)
        if isinstance(req, TxRequest):
            if req.request_type == TXFINISHED:
                break
            res = await ctx.call(req, TxAck)
        elif isinstance(req, UiConfirmOutput):
            res = await layout.confirm_output(ctx, req.output, req.coin)
            progress.report_init()
        elif isinstance(req, UiConfirmTotal):
            res = await layout.confirm_total(ctx, req.spending, req.fee, req.coin)
            progress.report_init()
        elif isinstance(req, UiConfirmFeeOverThreshold):
            res = await layout.confirm_feeoverthreshold(ctx, req.fee, req.coin)
            progress.report_init()
        elif isinstance(req, UiConfirmForeignAddress):
            res = await paths.show_path_warning(ctx, req.address_n)
        else:
            raise TypeError("Invalid signing instruction")
    return req
