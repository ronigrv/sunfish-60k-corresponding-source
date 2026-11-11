"""Encode the exact published Sunfish payload in UTF-8-safe seven-bit groups."""
import ast
import hashlib
import lzma
import pathlib

old = pathlib.Path("outputs/sunfish-60k-main.py").read_bytes().decode("latin1")
strings = [n.value for n in ast.walk(ast.parse(old))
           if isinstance(n, ast.Constant) and isinstance(n.value, str)
           and len(n.value) > 1000]
assert len(strings) == 1
payload = strings[0].encode("latin1")
assert hashlib.sha256(payload).hexdigest() == "eef1deba060a9ed20fe904a27703d07da52f5fc92f1be7c037f4b026b8376fb2"
bits = int.from_bytes(payload, "big")
groups = (len(payload)*8 + 6)//7
bits <<= groups*7 - len(payload)*8
values = [(bits >> (7*(groups-1-i))) & 127 for i in range(groups)]
unsafe = {0, 10, 13, 39, 92}
encoded = "".join(chr(n+128) if n in unsafe else chr(n) for n in values)
assert all(ord(c) % 128 == n for c, n in zip(encoded, values))
launcher = ("import lzma\nn=0\nfor c in '" + encoded +
            "':n=n*128+ord(c)%128\n"
            "exec(lzma.decompress(n.to_bytes(3353,'big')))\n")
program = launcher.encode("utf8")
assert len(program) <= 4096, len(program)
assert b"\x00" not in program
compile(program, "main.py", "exec")
entry = pathlib.Path("outputs/sunfish-utf8-main.py")
entry.write_bytes(program)
repository_entry = pathlib.Path("C:/Users/Roni/Documents/Codex/chess-fork-fresh-20261110/main.py")
template = repository_entry.read_text(encoding="utf8")
assert template.count("for c in '':") == 1
assembled = template.replace("for c in '':", "for c in '" + encoded + "':").encode("utf8")
assert assembled == program
repository_entry.write_bytes(assembled)
print("UTF-8 entry:", len(program), "bytes; exact payload sha256:",
      hashlib.sha256(payload).hexdigest())
