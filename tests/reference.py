"""Separate full-block-ID oracle with LRU lists, not compressed tags/ranks."""


class ReferenceCache:
    def __init__(self, config):
        self.config = config
        self.sets = [[] for _ in range(config.sets)]  # oldest -> newest

    def access(self, op, address):
        b = address // 32
        low = b % self.config.sets
        group = b // self.config.sets
        index = low ^ (group % self.config.sets) if self.config.mapping == "xor" else low
        entries = self.sets[index]
        hit = next((i for i, e in enumerate(entries) if e[0] == b), None)
        if hit is not None:
            entry = entries.pop(hit)
            entries.append((b, entry[1] or op == "W"))
            return True, None, None
        victim = entries.pop(0) if len(entries) == self.config.ways else None
        entries.append((b, op == "W"))
        return False, victim[0] if victim else None, victim[0] * 32 if victim and victim[1] else None
