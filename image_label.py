#!/usr/bin/env python3
"""App to add a label to one or more images"""

import argparse
import configparser
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys

config = configparser.ConfigParser()

# acceptable location values
# top, top right, right, bottom right, etc
locations = "T TR R BR B BL L TL".split()

# RGB values for colors
colors = {
    'red' : (255,0,0),
    'blue' : (0,0,255),
    'green' : (0,153,0),
    'yellow' : (255,255,0),
    'black' : (0,0,0),
    'white' : (255,255,255)
}

parser = argparse.ArgumentParser(
    description='Add a text label to an existing image',
    argument_default=argparse.SUPPRESS)
parser.add_argument('-T','--text', type=str, help='Label text')
parser.add_argument('-C','--color', choices=colors.keys(), help='Font color of the label text')
parser.add_argument('-S','--size', type=int, help='Integer: Font size of the label text')
parser.add_argument('-R','--offset_LR', type=int, help='Integer: Pixels to offset the label from the left and right of the image')
parser.add_argument('-B','--offset_TB', type=int, help='Integer: Pixels to offset the label from the top and bottom of the image')
parser.add_argument('-L','--location', choices=locations, help='Location of the label on the image')
parser.add_argument('-F','--fontfile', help='Path to TTF font file to use to generate the text label')
parser.add_argument('-s','--setting', type=str, help='Name of section heading in config.ini file')
args, files = parser.parse_known_args()

# get dict from Namespace object
parsed = vars(args)

config.read('config.ini')

def options():
    # using function object to host attributes instead of dict
    pass

# load the default config options
options.font_color = 'red'
options.font_file = './open-sans/OpenSans-Bold.ttf'
options.font_size = 100
options.label_location = 'TL'
options.label_offset_TB = 50
options.label_offset_LR = 50
options.label_text = 'DEFAULT TEXT'

# if the config file has a DEFAULTS section, override the internal
# defaults with those settings
if 'DEFAULTS' in config:
    if 'font_color' in config['DEFAULTS']:
        options.font_color = config['DEFAULTS']['font_color']
    if 'font_file' in config['DEFAULTS']:
        options.font_file = config['DEFAULTS']['font_file']
    if 'font_size' in config['DEFAULTS']:
        options.font_size = int(config['DEFAULTS']['font_size'])
    if 'label_location' in config['DEFAULTS']:
        options.label_location = config['DEFAULTS']['label_location']
    if 'label_offset_TB' in config['DEFAULTS']:
        options.label_offset_TB = int(config['DEFAULTS']['label_offset_TB'])
    if 'label_offset_LR' in config['DEFAULTS']:
        options.label_offset_LR = int(config['DEFAULTS']['label_offset_LR'])
    if 'label_text' in config['DEFAULTS']:
        options.label_text = config['DEFAULTS']['label_text']

# if settings option provided via CLI, override the options
# with the values from that section
if 'setting' in parsed:
    mysection = parsed['setting']
    if mysection in config:
        if 'font_color' in config[mysection]:
            options.font_color = config[mysection]['font_color']
        if 'font_file' in config[mysection]:
            options.font_file = config[mysection]['font_file']
        if 'font_size' in config[mysection]:
            options.font_size = int(config[mysection]['font_size'])
        if 'label_location' in config[mysection]:
            options.label_location = config[mysection]['label_location']
        if 'label_offset_TB' in config[mysection]:
            options.label_offset_TB = int(config[mysection]['label_offset_TB'])
        if 'label_offset_LR' in config[mysection]:
            options.label_offset_LR = int(config[mysection]['label_offset_LR'])
        if 'label_text' in config[mysection]:
            options.label_text = config[mysection]['label_text']
    else:
        print('ERROR: --setting value of {} is not included in the config file'.format(mysection))

# override the options with any CLI options
if 'text' in parsed:
    options.label_text = parsed['text']
if 'color' in parsed:
    options.label_color = parsed['color']
if 'size' in parsed:
    options.font_size = int(parsed['size'])
if 'offset_LR' in parsed:
    options.label_offset_LR = int(parsed['offset_LR'])
if 'offset_TB' in parsed:
    options.label_offset_TB = int(parsed['offset_TB'])
if 'location' in parsed:
    options.label_location = parsed['location']
if 'fontfile' in parsed:
    options.font_file = parsed['fontfile']

if not options.label_location in locations:
    print('Location choice of {} is not among acceptable values of {}'.format(options.label_location, locations))
    sys.exit(1)

img = Image.open("sample_in.jpg")
image_width, image_height = img.size
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(options.font_file, int(options.font_size))
text_width, text_height  = draw.textsize(options.label_text, font=font)

if (((options.label_offset_LR * 2) + text_width) > image_width):
    print('label_offset_LR on each side plus text width is too large to fit on this image')
    sys.exit(1)
    
if (((options.label_offset_TB * 2) + text_height) > image_height):
    print('label_offset_TB on top and bottom, plus text height is too large to fit on this image')
    sys.exit(1)

# establish print location x
if options.label_location in ['TL', 'L', 'BL']:
    x = options.label_offset_LR
elif options.label_location in ['T', 'B']:
    x = (image_width - text_width) / 2
elif options.label_location in ['TR', 'R', 'BR']:
    x = image_width - (text_width + options.label_offset_LR)

# establish print location y
if options.label_location in ['TL', 'T', 'TR']:
    y = options.label_offset_TB
elif options.label_location in ['L', 'R']:
    y = (image_height - text_height) / 2
elif options.label_location in ['BL', 'B', 'BR']:
    y = image_height - (text_height + options.label_offset_TB)

draw.text((x, y), options.label_text, colors[options.font_color], font=font)
img.save('sample_out.jpg')
