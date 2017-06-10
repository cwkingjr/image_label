#!/usr/bin/env python3
"""App to add a label to one or more images"""

import configparser
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys

config = configparser.ConfigParser()

config['default'] = {
    'text' : 'DEFAULT TEXT',
    'color' : 'red',
    'size' : 100,
    'offset_LR' : 50,
    'offset_TB' : 50,
    'location' : 'TL',
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

# acceptable location values
locations = "T TR R BR B BL L TL".split()

config.read('config.ini')

# validate all of these before production
text = config['default']['text']
size = int(config['default']['size'])
font_file = config['default']['font_file']
offset_TB = int(config['default']['offset_TB'])
offset_LR = int(config['default']['offset_LR'])
color = config['default']['color']
location = config['default']['location']

if not location in locations:
    print('Location choice of {} is not among acceptable values of {}'.format(location, locations))
    sys.exit(1)

img = Image.open("sample_in.jpg")
image_width, image_height = img.size
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(font_file, size)
text_width, text_height  = draw.textsize(text, font=font)

#print('text width', text_width)
#print('text height', text_height)
#print('image width', image_width)
#print('image height', image_height)

if (((offset_LR * 2) + text_width) > image_width):
    print('offset_LR on each side plus text width is too large to fit on this image')
    sys.exit(1)
    
if (((offset_TB * 2) + text_height) > image_height):
    print('offset_TB on top and bottom, plus text height is too large to fit on this image')
    sys.exit(1)

# establish print location x
if location in ['TL', 'L', 'BL']:
    x = offset_LR
elif location in ['T', 'B']:
    x = (image_width - text_width) / 2
elif location in ['TR', 'R', 'BR']:
    x = image_width - (text_width + offset_LR)

# establish print location y
if location in ['TL', 'T', 'TR']:
    y = offset_TB
elif location in ['L', 'R']:
    y = (image_height - text_height) / 2
elif location in ['BL', 'B', 'BR']:
    y = image_height - (text_height + offset_TB)

draw.text((x, y), text, colors[color], font=font)
img.save('sample_out.jpg')
