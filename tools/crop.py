"""Usage: python3 tools/crop.py <render.jpg> <out.png> [pixels_from_bottom=1900] [length=1300]"""
import sys
from PIL import Image
im=Image.open(sys.argv[1]); H=im.height; fb=int(sys.argv[3]) if len(sys.argv)>3 else 1900; ln=int(sys.argv[4]) if len(sys.argv)>4 else 1300
x0,x1=(280,1000) if im.width>900 else (0,im.width)
im.crop((x0,max(0,H-fb),x1,min(H,H-fb+ln))).save(sys.argv[2])
