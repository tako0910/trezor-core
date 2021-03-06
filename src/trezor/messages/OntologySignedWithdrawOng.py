# Automatically generated by pb2py
# fmt: off
import protobuf as p


class OntologySignedWithdrawOng(p.MessageType):
    MESSAGE_WIRE_TYPE = 357
    FIELDS = {
        1: ('signature', p.BytesType, 0),
        2: ('payload', p.BytesType, 0),
    }

    def __init__(
        self,
        signature: bytes = None,
        payload: bytes = None,
    ) -> None:
        self.signature = signature
        self.payload = payload
