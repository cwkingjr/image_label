#!/usr/bin/env python3
"""App to add a label to one or more images"""

import argparse
import configparser
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageStat
import os
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
acceptable_colors = sorted(colors.keys())

# http://pillow.readthedocs.io/en/3.1.x/handbook/image-file-formats.html
output_formats = 'BMP JPEG PNG'.split()

parser = argparse.ArgumentParser(
    description='Add a text label to an existing image. Optionally, also rotate the image.',
    argument_default=argparse.SUPPRESS)

parser.add_argument('-S','--setting', type=str, help='Name of section in config file to use.')
parser.add_argument('-T','--label_text', type=str, help='Label text')
parser.add_argument('-L','--label_location', choices=locations, help='Location of the label on the image.')
parser.add_argument('-C','--font_color', choices=colors.keys(), help='Font color of the label text.')
parser.add_argument('-F','--font_file', help='Path to TTF font file to use to generate the text label.')
parser.add_argument('-Z','--font_size', type=int, help='Integer: Font size of the label text.')
parser.add_argument('-H','--label_offset_LR', type=int, help='Integer: Pixels to offset the label from the left and right of the image.')
parser.add_argument('-V','--label_offset_TB', type=int, help='Integer: Pixels to offset the label from the top and bottom of the image.')
parser.add_argument('-R','--rotate', type=int, help='Integer: Degrees to rotate image clockwise [1-359].')
parser.add_argument('-J','--jpg_quality', type=int, help='Integer: JPG quality [1-95]. Default is 93. Larger affects output file size but may not improve actual quality. Quality cannot get better than the original image.')
parser.add_argument('-B','--black_for_BW', action='store_true', help='Use black as text color for black and white images. Default is white.')
parser.add_argument('-I','--list_ini_sections', action='store_true', help='List the sections in your config file for convenience.')
parser.add_argument('-O','--output_format', choices=output_formats, help='Output file format. Default is JPEG.')

args, files = parser.parse_known_args()

# get dict from Namespace object
parsed = vars(args)

if 'IMAGE_LABEL_CONFIG' in os.environ:
    config.read(os.environ['IMAGE_LABEL_CONFIG'])
else:
    print('Could not find environment variable of IMAGE_LABEL_CONFIG so could not read config file')

if 'list_ini_sections' in parsed:
    print(' '.join(sorted(config.sections())))
    sys.exit(0)

# using function object to host options as attributes instead of dict k:v
def options():
    pass

# set the internal default config options
options.font_color = 'red'
options.font_file = './open-sans/OpenSans-Bold.ttf'
options.font_size = 100
options.label_location = 'TL'
options.label_offset_TB = 50
options.label_offset_LR = 50
options.label_text = 'DEFAULT TEXT'
options.rotate = None
options.jpg_quality = 93
options.black_for_BW = False
options.output_format = 'JPEG'

def load_settings_values(mydict):
    if 'font_color' in mydict:
        options.font_color = mydict['font_color']
    if 'font_file' in mydict:
        options.font_file = mydict['font_file']
    if 'font_size' in mydict:
        options.font_size = int(mydict['font_size'])
    if 'label_location' in mydict:
        options.label_location = mydict['label_location']
    if 'label_offset_TB' in mydict:
        options.label_offset_TB = int(mydict['label_offset_TB'])
    if 'label_offset_LR' in mydict:
        options.label_offset_LR = int(mydict['label_offset_LR'])
    if 'label_text' in mydict:
        options.label_text = mydict['label_text']
    if 'rotate' in mydict:
        options.rotate = mydict['rotate']
    if 'jpg_quality' in mydict:
        options.jpg_quality = mydict['jpg_quality']
    if 'black_for_BW' in mydict:
        options.black_for_BW = mydict['black_for_BW']
    if 'output_format' in mydict:
        options.output_format = mydict['output_format']

# if the config file has a DEFAULTS section, override the internal
# defaults with those settings
if 'DEFAULTS' in config:
    load_settings_values(config['DEFAULTS'])

# if setting option provided via CLI, override the current options
# with the values from that section
if 'setting' in parsed:
    mysection = parsed['setting']
    if mysection in config:
        load_settings_values(config[mysection])
    else:
        print('ERROR: --setting value of {} is not included in the config file'.format(mysection))

# override the current options with any CLI options
load_settings_values(parsed)

if not options.font_color in acceptable_colors:
    print('Font color choice of {} is not among acceptable values of {}'.format(options.font_color, acceptable_colors))
    sys.exit(1)

if not options.label_location in locations:
    print('Location choice of {} is not among acceptable values of {}'.format(options.label_location, locations))
    sys.exit(1)

if options.rotate:
    if not 0 < options.rotate < 360:
        print('ERROR: --rotate must be between 1-359 inclusive')
        sys.exit(1)

if not 1 <= options.jpg_quality <= 95:
    print('jgp_quality must be between 1-95. This will affect image quality and output jpg/jpeg file size')
    sys.exit(1)

# make sure entries from setting file are correct and converted to bool
if type(options.black_for_BW) == str:
    if options.black_for_BW == 'True':
        options.black_for_BW = True
    elif options.black_for_BW == 'False':
        options.black_for_BW = False
    else:
        print('ERROR: When setting black_for_BW via config file, it must be set to True or False')
        sys.exit(1)

if not options.output_format in output_formats:
    print('ERROR: Output format {} is not valid, choose from {}'.format(options.output_format, output_formats))
    sys.exit(1)

# test ttf file to make sure it's a ttf file using magic bytes
true_type_font_magic = b'\x00\x01\x00\x00'
with open(options.font_file,'rb') as f:
    bites = f.read(4)
    if bites != true_type_font_magic:
        print('The font file provided does not appear to be a True Type Font file')
        sys.exit(1)

# https://stackoverflow.com/questions/20068945/
# detect-if-image-is-color-grayscale-or-black-and-white-with-python-pil
def is_black_and_white(myimg):
    # choosing 200 because I had some color images that only had ~500 v
    COLOR_VARIANCE_THRESHOLD = 200

    v = ImageStat.Stat(myimg).var
    maxmin = abs(max(v) - min(v))
    
    if len(v) == 1:
        return True
    elif maxmin < COLOR_VARIANCE_THRESHOLD:
        return True
    else:
        return False
    
def process_file(filename):
    img = Image.open(filename)

    if options.rotate:
        # rotation is ccw but can take negative numbers for cw, so multi input by -1
        # expand prevents truncation of image but can result in black borders
        img = img.rotate(int(options.rotate) * -1, expand=True)

    image_width, image_height = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(options.font_file, int(options.font_size))
    text_width, text_height = draw.textsize(options.label_text, font=font)

    if options.label_offset_LR * 2 + text_width > image_width:
        print('label_offset_LR * 2, plus text width is too large to fit on {}'.format(filename))
        sys.exit(1)
    
    if options.label_offset_TB * 2 + text_height > image_height:
        print('label_offset_TB * 2, plus text height is too large to fit on {}'.format(filename))
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

    if is_black_and_white(img):
        # when the image is black and white, draw.text must provide a single color,
        # not the 3-tuple RGB color, it will blow up
        if options.black_for_BW:
            bwcolor = 0
            bwcolortext = 'black'
        else:
            bwcolor = 255
            bwcolortext = 'white'

        print('Image appears to be black and white, which cannot take RGB text, so using {} as text color'.format(bwcolortext))
        draw.text((x, y), options.label_text, bwcolor, font=font)
    else:
        draw.text((x, y), options.label_text, colors[options.font_color], font=font)

    # add 'altered' to filename to prevent overwriting original
    if '.' in os.path.basename(filename):
        path,_ = os.path.splitext(filename)
        outfilename = "{}.altered.{}".format(path, options.output_format)
    else:
        outfilename = "{}.altered".format(path)

    # of BMP JPEG PNG only JPEG consumes the 'quality' parameter
    img.save(outfilename, format=options.output_format, quality=options.jpg_quality)

for filename in files:
    process_file(filename)