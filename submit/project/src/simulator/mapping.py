"""Placement and inverse mapping; never derive XOR writebacks as modulo."""

from .models import Config


class Mapping:
    def __init__(self, config: Config):
        self.config = config

    def split(self, address):
        block = address >> 5
        if self.config.mapping == "xor":
            return block, (block ^ (block >> 6)) & 63, block >> 6
        return block, block % self.config.sets, block // self.config.sets

    def recover_block(self, index, tag):
        if self.config.mapping == "xor":
            return (tag << 6) | (index ^ (tag & 63))
        return tag * self.config.sets + index
