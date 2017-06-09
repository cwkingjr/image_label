#!/usr/bin/env python3
"""App to add a label to one or more images"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

img = Image.open("sample_in.jpg")
draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("./open-sans/OpenSans-Bold.ttf", 150)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((30, 0), "TOP", (255, 0, 0), font=font)
img.save('sample_out.jpg')
