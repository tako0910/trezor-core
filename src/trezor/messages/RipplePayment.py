# Automatically generated by pb2py
# fmt: off
import protobuf as p


class RipplePayment(p.MessageType):

    def __init__(
        self,
        amount: int = None,
        destination: str = None,
    ) -> None:
        self.amount = amount
        self.destination = destination

    @classmethod
    def get_fields(cls):
        return {
            1: ('amount', p.UVarintType, 0),
            2: ('destination', p.UnicodeType, 0),
        }
