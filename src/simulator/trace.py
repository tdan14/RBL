"""Strict UTF-8 trace parser. Blank lines and # comments do not count."""

from dataclasses import dataclass
from pathlib import Path

from .models import validate_access


@dataclass(frozen=True)
class TraceAccess:
    operation: str
    address: int
    size: int
    line_number: int


def read_trace(path):
    with Path(path).open(encoding="utf-8-sig") as stream:
        for number, raw in enumerate(stream, 1):
            text = raw.split("#", 1)[0].strip()
            if not text:
                continue
            try:
                parts = text.split()
                if len(parts) != 3:
                    raise ValueError("Expected OP ADDRESS SIZE")
                op, address_text, size_text = parts
                address = int(address_text, 16 if address_text.lower().startswith("0x") else 10)
                size = int(size_text, 10)
                validate_access(op, address, size)
            except ValueError as error:
                raise ValueError(f"{path}: line {number}: {error}") from error
            yield TraceAccess(op, address, size, number)
