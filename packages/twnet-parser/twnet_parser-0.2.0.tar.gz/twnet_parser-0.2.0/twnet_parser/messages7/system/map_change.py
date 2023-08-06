#!/usr/bin/env python

from twnet_parser.pretty_print import PrettyPrint
from twnet_parser.packer import Unpacker

class MsgMapChange(PrettyPrint):
    def __init__(
            self,
            name: str = 'dm1',
            crc: int = -1,
            size: int = 1337,
            chunks_per_request: int = 8,
            chunk_size: int = 1384,
            sha256: bytes = bytes(32)
    ) -> None:
        self.message_name = 'map_change'
        self.name = name
        self.crc = crc
        self.size = size
        self.chunks_per_request = chunks_per_request
        self.chunk_size = chunk_size
        self.sha256 = sha256

    # first byte of data
    # has to be the first byte of the message payload
    # NOT the chunk header and NOT the message id
    def unpack(self, data: bytes) -> bool:
        unpacker = Unpacker(data)
        self.name = unpacker.get_str()
        self.crc = unpacker.get_int()
        self.size = unpacker.get_int()
        self.chunks_per_request = unpacker.get_int()
        return True

    def pack(self) -> bytes:
        return b'todo'

# msg = MsgMapChange()
# msg.unpack(
#         b'BlmapChill\x00' \
#         b'\xde\xcf\xaa\xee\x0b' \
#         b'\x8b\xbe\x8a\x01' \
#         b'\x08' \
#         b'\xa8\x15' \
#         b'\x81\x7d\xbf\x48\xc5\xf1\x94\x37\xc4\x58\x2c\x6f\x98\xc9\xc2\x04\xc1\xf1\x69\x76\x32\xf0\x44\x58\x74\x54\x55\x89\x84\x00\xfb\x28')
# 
# print(msg)
