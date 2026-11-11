"""Rebuild the 30k-node make.fun experiment from its readable source."""
import hashlib
import lzma
from pathlib import Path
import python_minifier

source = Path('sunfish-30k.py').read_text(encoding='utf8')
text = python_minifier.minify(source, rename_globals=True,
    remove_literal_statements=True, hoist_literals=False,
    preserve_globals=['choose_game'])
packed = lzma.compress(text.encode(), format=lzma.FORMAT_ALONE,
    filters=[{'id':lzma.FILTER_LZMA1, 'dict_size':1 << 20, 'lc':3, 'lp':0, 'pb':0}])
assert hashlib.sha256(packed).hexdigest() == 'e3eceb98dfac69a8ae4cf9849d670df23c0a41f0eb995a79119618130f097d6a'
groups = (len(packed)*8 + 6)//7
number = int.from_bytes(packed,'big') << (groups*7-len(packed)*8)
values = [(number >> (7*(groups-1-i))) & 127 for i in range(groups)]
encoded = ''.join(chr(n+128) if n in {0,10,13,39,92} else chr(n) for n in values)
output = ("import lzma\nn=0\nfor c in '"+encoded+"':n=n*128+ord(c)%128\n"
          + f"exec(lzma.decompress(n.to_bytes({len(packed)},'big')))\n").encode('utf8')
assert len(output) <= 4096
compile(output,'main.py','exec')
Path('sunfish-30k-entry.py').write_bytes(output)
print('bytes:',len(output),'SHA-256:',hashlib.sha256(output).hexdigest())
