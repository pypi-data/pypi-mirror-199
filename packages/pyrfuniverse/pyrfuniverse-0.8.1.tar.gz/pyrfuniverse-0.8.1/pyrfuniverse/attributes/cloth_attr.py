import pyrfuniverse.attributes as attr
from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)


class ClothAttr(attr.BaseAttr):
    """
    ObiCloth类
    """
    def parse_message(self, msg: IncomingMessage) -> dict:
        super().parse_message(msg)
        return self.data