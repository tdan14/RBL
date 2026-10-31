"""Frozen synthetic workloads and separate line-number-based validator."""

from itertools import islice
import random

COUNT = 110000


def scenarios():
    items = []
    for op in ("R", "W"):
        items.append(dict(trace_id=f"W1-{'read' if op == 'R' else 'write'}", family="W1", op=op, base=0x10000000, seed=None))
    for size in (1024, 4096, 16384):
        items.append(dict(trace_id=f"W2-{size}", family="W2", buffer_bytes=size, base=0x20000000, seed=None))
    for window in (8, 32, 128, 512, 2048):
        items.append(dict(trace_id=f"W3-N{window}", family="W3", window=window, ring_samples=4096, base=0x30000000, seed=None))
    items.append(dict(trace_id="W4-even", family="W4", random=False, base=0x40000000, seed=None))
    for seed in range(1, 11):
        items.append(dict(trace_id=f"W4-random-S{seed:02d}", family="W4", random=True, base=0x40000000, seed=seed))
    for blocks in (2, 4, 8):
        items.append(dict(trace_id=f"W5-K{blocks}", family="W5", blocks=blocks, stride=4096, base=0x50000000, seed=None))
    return items


def accesses(spec):
    base = spec["base"]
    if spec["family"] == "W1":
        address = base
        while True:
            yield spec["op"], address, 4
            address += 4
    elif spec["family"] == "W2":
        while True:
            for address in range(base, base + spec["buffer_bytes"], 4):
                yield "R", address, 4
    elif spec["family"] == "W3":
        sample = 0
        while True:
            yield "W", base + sample * 4, 4
            for age in range(spec["window"]):
                yield "R", base + ((sample - age) % spec["ring_samples"]) * 4, 4
            sample = (sample + 1) % spec["ring_samples"]
    elif spec["family"] == "W4":
        rng = random.Random(spec["seed"])
        pointers = [0] * 4
        step = 0
        while True:
            sensor = rng.randrange(4) if spec["random"] else step % 4
            yield "W", base + sensor * 1024 + pointers[sensor] * 4, 4
            pointers[sensor] = (pointers[sensor] + 1) % 256
            step += 1
    else:
        while True:
            for block in range(spec["blocks"]):
                yield "R", base + block * spec["stride"], 4


def encoded_trace(spec, count=COUNT):
    for op, address, size in islice(accesses(spec), count):
        yield f"{op} 0x{address:08X} {size}\n".encode("ascii")


def validate_trace(spec, parsed):
    """Check by access number, not by calling the generator under test."""
    reads = writes = 0
    minimum, maximum = 2**32, -1
    rng = random.Random(spec["seed"])
    sensor_counts = [0] * 4
    count = 0
    for i, access in enumerate(parsed):
        base, family = spec["base"], spec["family"]
        if family == "W1":
            op, address = spec["op"], base + 4 * i
        elif family == "W2":
            op, address = "R", base + (i * 4) % spec["buffer_bytes"]
        elif family == "W3":
            cycle, position = divmod(i, spec["window"] + 1)
            op = "W" if position == 0 else "R"
            slot = cycle if position == 0 else cycle - position + 1
            address = base + (slot % spec["ring_samples"]) * 4
        elif family == "W4":
            sensor = rng.randrange(4) if spec["random"] else i % 4
            op, address = "W", base + sensor * 1024 + (sensor_counts[sensor] % 256) * 4
            sensor_counts[sensor] += 1
        else:
            op, address = "R", base + (i % spec["blocks"]) * 4096
            if (address // 32) % 128 != (base // 32) % 128:
                raise AssertionError("W5 does not collide in D0")
        if (access.operation, access.address, access.size) != (op, address, 4):
            raise AssertionError(f"{spec['trace_id']} access {i}: spec mismatch")
        reads += int(op == "R"); writes += int(op == "W")
        minimum, maximum = min(minimum, address), max(maximum, address)
        count += 1
    if count != COUNT:
        raise AssertionError(f"Expected {COUNT}, found {count}")
    return dict(access_count=count, reads=reads, writes=writes, min_address=minimum,
                max_address=maximum, sensor_access_counts=sensor_counts if spec["family"] == "W4" else None)
