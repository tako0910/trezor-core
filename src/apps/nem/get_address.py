from trezor.messages.NEMAddress import NEMAddress

from .helpers import NEM_CURVE, check_path, get_network_str
from .validators import validate_network

from apps.common import seed
from apps.common.layout import show_address, show_qr
from apps.common.paths import validate_path


async def get_address(ctx, msg):
    network = validate_network(msg.network)
    node = await seed.derive_node(ctx, msg.address_n, NEM_CURVE)
    address = node.nem_address(network)

    await validate_path(ctx, check_path, path=msg.address_n, network=msg.network)

    if msg.show_display:
        while True:
            if await show_address(ctx, address, get_network_str(network)):
                break
            if await show_qr(ctx, address.upper()):
                break

    return NEMAddress(address=address)
