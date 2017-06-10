#!/usr/bin/env python3
"""App to add a label to one or more images"""

import configparser
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

config = configparser.ConfigParser()

config['default'] = {
    'text' : 'Default Insertion Text',
    'color' : 'red',
    'size' : 150,
    'offset' : 50,
    'location' : 'NW',
    'font_file' : './open-sans/OpenSans-Bold.ttf'
}

# RGB values for colors
colors = {
    'red' : (255,0,0),
    'blue' : (0,0,255),
    'green' : (0,153,0),
    'yellow' : (255,255,0),
    'black' : (0,0,0),
    'white' : (255,255,255)
}

config.read('config.ini')

print(config.sections())

# validate all of these before production
text = config['default']['text']
size = int(config['default']['size'])
font_file = config['default']['font_file']
offset = int(config['default']['offset'])
color = config['default']['color']

img = Image.open("sample_in.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(font_file, size)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((offset, 0), text, colors[color], font=font)
img.save('sample_out.jpg')
