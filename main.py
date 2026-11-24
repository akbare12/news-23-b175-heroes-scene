#!/usr/bin/env python3
"""Entry-point for THE WORLD TODAY — Monday 23 November 2026 (31 stories).

Stdlib only (no PIL). Verifies the bundled entry.png byte-for-byte
(struct PNG header parse + chunk-walk CRC checks) and writes a copy to
MAKEFUN_OUTPUT_DIR/entry.png. Never writes next to main.py.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "8f888daf3bd2ce704311125962efb02777c04e418dd5a937d6fbe21d62e853e4"
EXPECTED_SIZE = 147603
MIN_SIZE = 10_000
MAX_SIZE = 1_048_576


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def check_png(data):
    if len(data) < MIN_SIZE:
        fail(f"entry.png too small: {len(data)} bytes")
    if len(data) > MAX_SIZE:
        fail(f"entry.png too large: {len(data)} bytes")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    # first chunk must be IHDR, 13 bytes, 1024x1024, 8-bit, colour 2/6
    ln, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or ln != 13:
        fail("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype2, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        fail(f"wrong dimensions: {w}x{h}")
    if depth != 8 or ctype2 not in (2, 6):
        fail(f"unexpected bit depth {depth} / colour type {ctype2}")
    if comp != 0 or filt != 0 or inter != 0:
        fail("unexpected compression/filter/interlace flag")
    crc_stored = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != crc_stored:
        fail("IHDR CRC mismatch")
    # chunk walk: CRC each chunk, IDAT payloads non-empty, IEND last
    pos, idat_total, saw_iend = 8, 0, False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        ln, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if pos + 12 + ln > len(data):
            fail(f"truncated chunk {ctype!r}")
        crc_stored = struct.unpack(">I", data[pos + 8 + ln:pos + 12 + ln])[0]
        if zlib.crc32(ctype + data[pos + 8:pos + 8 + ln]) & 0xFFFFFFFF != crc_stored:
            fail(f"CRC mismatch in chunk {ctype!r}")
        if ctype == b"IDAT":
            if ln == 0:
                fail("empty IDAT chunk")
            idat_total += ln
        if ctype == b"IEND":
            if ln != 0:
                fail("IEND must be empty")
            if pos + 12 + ln != len(data):
                fail("trailing data after IEND")
            saw_iend = True
            break
        pos += 12 + ln
    if not saw_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail(f"IDAT payload too small: {idat_total} bytes")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repository")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR exists and is not a directory")
    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail(f"cannot read entry.png: {exc}")
    check_png(data)
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        fail(f"sha256 mismatch: got {sha}")
    if len(data) != EXPECTED_SIZE:
        fail(f"size mismatch: got {len(data)}, expected {EXPECTED_SIZE}")
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source image")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        fail("output does not match the source byte-for-byte")
    print(f"ok: entry.png {len(data)} bytes sha256 {sha}")


if __name__ == "__main__":
    main()
