#!/usr/bin/env python3
"""App to add a label to one or more images"""

import configparser
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys

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

# acceptable location values
locations = "N NE E SE S SW W NW".split()

config.read('config.ini')

# validate all of these before production
text = config['default']['text']
size = int(config['default']['size'])
font_file = config['default']['font_file']
offset = int(config['default']['offset'])
color = config['default']['color']
location = config['default']['location']

# temp for testing
location = 'NE'

# validations
if not location in locations:
    print('Location choice of {} is not among acceptable values of {}'.format(location, locations))
    sys.exit(1)

img = Image.open("sample_in.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(font_file, size)

width, height = img.size
#print('image width', width)
#print('image height', height)

# TODO determine size of text to be printed and deduct that from x,y
# to allow space for the text when on the right side of the drawing

# establish print location x coordinate
if location in ['NW', 'W', 'SW']:
    x = offset
elif location in ['N', 'S']:
    x = width / 2
elif location in ['NE', 'E', 'SE']:
    x = width - offset

# establish print location y coordinate
if location in ['NW', 'N', 'NE']:
    y = offset
elif location in ['W', 'E']:
    y = height / 2
elif location in ['SW', 'S', 'SE']:
    y = height - offset

draw.text((x, y), text, colors[color], font=font)
img.save('sample_out.jpg')
