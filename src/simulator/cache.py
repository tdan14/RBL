"""Shared cache engine: exact 2-way bit LRU and 4-way rank LRU."""

from dataclasses import asdict, dataclass

from .mapping import Mapping
from .models import CacheLine, Config, Counters, validate_access


@dataclass(frozen=True)
class AccessResult:
    operation: str
    address: int
    block: int
    index: int
    tag: int
    way: int
    hit: bool
    measured: bool
    victim_block: int | None = None
    writeback_base: int | None = None
    fill_base: int | None = None

    def snapshot(self):
        return asdict(self)


class Cache:
    def __init__(self, config: Config):
        self.config = config
        self.mapping = Mapping(config)
        self.reset_run()

    def reset_run(self):
        self.lines = [[CacheLine() for _ in range(self.config.ways)] for _ in range(self.config.sets)]
        self.lru_way = [0] * self.config.sets if self.config.ways == 2 else []
        self.counters = Counters()
        self.measuring = False

    def begin_measurement(self):
        self.counters = Counters()
        self.measuring = True

    def _inc(self, name):
        if self.measuring:
            setattr(self.counters, name, getattr(self.counters, name) + 1)

    def _touch(self, index, way, was_valid):
        if self.config.ways == 2:
            self.lru_way[index] = 1 - way
        elif self.config.ways == 4:
            lines = self.lines[index]
            old_rank = lines[way].rank if was_valid else self.config.ways
            for other_way, line in enumerate(lines):
                if other_way != way and line.valid and line.rank < old_rank:
                    line.rank += 1
            lines[way].rank = 0

    def access(self, op, address, size=4):
        validate_access(op, address, size)  # No mutation before validation.
        block, index, tag = self.mapping.split(address)
        lines = self.lines[index]
        matches = [w for w, line in enumerate(lines) if line.valid and line.tag == tag]
        if len(matches) > 1:
            raise AssertionError("Duplicate block in a set")
        self._inc("accesses")
        if matches:
            way = matches[0]
            self._inc("hits")
            if op == "W":
                lines[way].dirty = True
            self._touch(index, way, True)
            return AccessResult(op, address, block, index, tag, way, True, self.measuring)

        self._inc("misses")
        self._inc("read_misses" if op == "R" else "write_misses")
        invalid = [w for w, line in enumerate(lines) if not line.valid]
        if invalid:
            way = min(invalid)
        elif self.config.ways == 1:
            way = 0
        elif self.config.ways == 2:
            way = self.lru_way[index]
        else:
            way = max(range(4), key=lambda w: lines[w].rank)
        victim = lines[way]
        victim_block = writeback_base = None
        was_valid = victim.valid
        if was_valid:
            victim_block = self.mapping.recover_block(index, victim.tag)
            self._inc("evictions")
            if victim.dirty:
                writeback_base = victim_block << 5
                self._inc("dirty_writebacks")
        # The eviction result captures the old address before overwriting tag.
        self._inc("line_fills")
        self._touch(index, way, was_valid)
        victim.valid, victim.tag, victim.dirty = True, tag, op == "W"
        return AccessResult(op, address, block, index, tag, way, False,
                            self.measuring, victim_block, writeback_base, block << 5)

    def check_invariants(self):
        self.counters.validate()
        for index, lines in enumerate(self.lines):
            tags = [line.tag for line in lines if line.valid]
            if len(tags) != len(set(tags)):
                raise AssertionError("Duplicate valid tag")
            if self.config.ways == 4:
                ranks = sorted(line.rank for line in lines if line.valid)
                if ranks != list(range(len(ranks))):
                    raise AssertionError("Invalid exact LRU ranks")
            for line in lines:
                if line.valid:
                    b = self.mapping.recover_block(index, line.tag)
                    if self.mapping.split(b << 5)[1:] != (index, line.tag):
                        raise AssertionError("Invalid block placement")

    def metrics(self, *, validate=True):
        if validate:
            self.check_invariants()
        c = self.counters
        return {
            "hit_rate": c.hits / c.accesses if c.accesses else None,
            "miss_rate": c.misses / c.accesses if c.accesses else None,
            "memory_traffic_bytes": (c.line_fills + c.dirty_writebacks) * 32,
            "metadata_logic_bytes": self.config.metadata_bytes,
        }
