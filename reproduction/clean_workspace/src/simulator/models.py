"""Validated frozen configurations and cache state."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Config:
    design_id: str
    sets: int
    ways: int
    mapping: str
    capacity_bytes: int = 4096
    line_bytes: int = 32
    write_policy: str = "write-back"
    allocation: str = "write-allocate"
    replacement: str = "LRU"
    prefetch: bool = False
    bypass: bool = False

    def __post_init__(self):
        expected = {
            "D0": (128, 1, "modulo"), "D1": (64, 2, "modulo"),
            "D2": (32, 4, "modulo"), "DAI-v1": (64, 2, "xor"),
        }
        for name in ("sets", "ways", "capacity_bytes", "line_bytes"):
            if type(getattr(self, name)) is not int:
                raise ValueError(f"{name} must be an integer")
        if self.design_id not in expected or (self.sets, self.ways, self.mapping) != expected[self.design_id]:
            raise ValueError("Configuration does not match a frozen design")
        if self.capacity_bytes != 4096 or self.line_bytes != 32 or self.sets * self.ways * self.line_bytes != 4096:
            raise ValueError("All designs require 4096 data bytes and 32-byte lines")
        if (self.write_policy, self.allocation, self.replacement) != ("write-back", "write-allocate", "LRU"):
            raise ValueError("Unsupported write/replacement policy")
        if self.prefetch is not False or self.bypass is not False:
            raise ValueError("Prefetch and bypass must be disabled")

    @classmethod
    def load(cls, path):
        return cls(**json.loads(Path(path).read_text(encoding="utf-8-sig")))

    def snapshot(self):
        return asdict(self)

    @property
    def metadata_bytes(self):
        tag_bits = 27 - (self.sets.bit_length() - 1)
        replacement_bits = {1: 0, 2: self.sets, 4: self.sets * 4 * 2}[self.ways]
        return (128 * (tag_bits + 2) + replacement_bits) // 8


@dataclass
class CacheLine:
    valid: bool = False
    dirty: bool = False
    tag: int = 0
    rank: int = 0  # D2 only: 0 = MRU; valid ranks are contiguous.


@dataclass
class Counters:
    accesses: int = 0
    hits: int = 0
    misses: int = 0
    read_misses: int = 0
    write_misses: int = 0
    evictions: int = 0
    dirty_writebacks: int = 0
    line_fills: int = 0

    def snapshot(self):
        return asdict(self)

    def validate(self):
        if not (self.hits + self.misses == self.accesses
                and self.read_misses + self.write_misses == self.misses
                and self.line_fills == self.misses
                and 0 <= self.dirty_writebacks <= self.evictions <= self.misses):
            raise AssertionError("Counter invariants violated")


def validate_access(op, address, size=4):
    if op not in ("R", "W") or type(address) is not int or type(size) is not int:
        raise ValueError("Access requires R/W, integer address and integer size")
    if size != 4 or not 0 <= address <= 0xFFFFFFFC or address % 4:
        raise ValueError("Access must be aligned 4 bytes within unsigned 32-bit memory")
