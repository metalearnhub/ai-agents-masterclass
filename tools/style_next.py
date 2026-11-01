"""Which blog style (A, B or C) the next post uses. Rotates A -> B -> C -> A by the most recent post's meta.json "style" (missing = A).
Usage: python3 tools/style_next.py   -> prints A, B or C. See STYLES.md."""
import json,glob,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ms=[json.load(open(f)) for f in glob.glob(os.path.join(R,'posts','*','meta.json'))]
ms=[m for m in ms if 'date' in m]
last=max(ms,key=lambda m:(m['date'],m.get('style','A')))
print({'A':'B','B':'C','C':'A'}[last.get('style','A').upper()])
