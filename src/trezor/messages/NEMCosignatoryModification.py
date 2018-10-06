# Automatically generated by pb2py
# fmt: off
import protobuf as p


class NEMCosignatoryModification(p.MessageType):

    def __init__(
        self,
        type: int = None,
        public_key: bytes = None,
    ) -> None:
        self.type = type
        self.public_key = public_key

    @classmethod
    def get_fields(cls):
        return {
            1: ('type', p.UVarintType, 0),
            2: ('public_key', p.BytesType, 0),
        }
