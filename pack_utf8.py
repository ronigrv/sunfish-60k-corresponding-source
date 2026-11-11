"""Reproduce the UTF-8-safe single-file competition entry from readable source.

This is a reproduction tool written after the original build.  The original
build scripts are retained separately so the build history is not obscured.
"""
import argparse
import hashlib
import lzma
from pathlib import Path

import python_minifier

SOURCE_SHA256 = "932c9c30a4289a3eba4800ad7506391c9582c583f1b2c5eee744b50d3a0d09e3"
PAYLOAD_SHA256 = "eef1deba060a9ed20fe904a27703d07da52f5fc92f1be7c037f4b026b8376fb2"
ENTRY_SHA256 = "1eff75f7b55048ad9312edf195df9ed885b4026d8655e621b223658229c3341c"

parser = argparse.ArgumentParser()
parser.add_argument("--source", default="work/sunfish-60k.py")
parser.add_argument("--output", default="sunfish-utf8-main.py")
args = parser.parse_args()
raw = Path(args.source).read_bytes()
if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
    raise ValueError("Readable source differs from the tested source")
source = raw.decode("utf8")
minified = python_minifier.minify(
    source, rename_globals=True, remove_literal_statements=True,
    hoist_literals=False, preserve_globals=["choose_game"])
filters = [{"id": lzma.FILTER_LZMA1, "dict_size": 1 << 20,
            "lc": 3, "lp": 0, "pb": 0}]
payload = lzma.compress(minified.encode(), format=lzma.FORMAT_ALONE, filters=filters)
if hashlib.sha256(payload).hexdigest() != PAYLOAD_SHA256:
    raise ValueError("Compressed payload differs; check Python, minifier and LZMA versions")
groups = (len(payload) * 8 + 6) // 7
value = int.from_bytes(payload, "big") << (groups * 7 - len(payload) * 8)
unsafe = {0, 10, 13, 39, 92}
encoded = "".join(chr(n + 128) if n in unsafe else chr(n)
                  for n in ((value >> (7 * (groups - 1 - i))) & 127
                            for i in range(groups)))
program = ("import lzma\nn=0\nfor c in '" + encoded +
           "':n=n*128+ord(c)%128\n"
           "exec(lzma.decompress(n.to_bytes(3353,'big')))\n").encode("utf8")
if len(program) > 4096 or hashlib.sha256(program).hexdigest() != ENTRY_SHA256:
    raise ValueError("Rebuilt entry differs from the tested 4 KB candidate")
compile(program, "main.py", "exec")
Path(args.output).write_bytes(program)
print("Reproduced", len(program), "bytes, SHA-256", ENTRY_SHA256)
