from typing import cast

import twnet_parser.msg7
import twnet_parser.messages7.system.map_change
from twnet_parser.net_message import NetMessage

# could also be named ChunkParser
class MessageParser():
    # the first byte of data has to be the
    # first byte of a message PAYLOAD
    # NOT the whole packet with packet header
    # and NOT the whole message with chunk header
    def parse_game_message(self, msg_id: int, data: bytes) -> NetMessage:
        raise ValueError(f"Error: unknown message game.id={msg_id} data={data[0]}")
    def parse_sys_message(self, msg_id: int, data: bytes) -> NetMessage:
        if msg_id == twnet_parser.msg7.MAP_CHANGE:
            msg = twnet_parser.messages7.system.map_change.MsgMapChange()
            msg.unpack(data)
            return cast(NetMessage, msg)
        raise ValueError(f"Error: unknown message sys.id={msg_id} data={data[0]}")

