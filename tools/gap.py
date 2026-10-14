"""Check the space between the article end and the newsletter on a full-page render.
Usage: python3 tools/gap.py <render.jpg> <width: 1280|420>
Prints the largest blank vertical runs in the lower half of the page.
Normal: ~110-150 px (desktop) / ~90-120 px (mobile) right before 'Get one practical idea...'.
Bigger -> reduce eb height by (gap - 130 / 100). If the article overlaps the newsletter there is
no big gap at all: crop the bottom and look (tools/crop.py) and increase the height."""
import sys,numpy as np
from PIL import Image
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int); H=a.shape[0]; w=int(sys.argv[2])
x0,x1=(300,980) if w>900 else (10,410)
nonw=(np.abs(a[:,x0:x1]-255).sum(2)>40).any(1)
runs=[];s=None
for y in range(H//2,H):
    if not nonw[y]: s=y if s is None else s
    elif s is not None: runs.append((y-s,s,y)); s=None
runs.sort(reverse=True); print('height',H,'largest blank runs (len,start,end):',runs[:4])
