#!/usr/bin/env python3
"""App to add a label to one or more images. Optionally rotates image and converts output format."""

# https://github.com/cwkingjr/image_label
# License: MIT, see LICENSE file

import argparse
import configparser
import os
from os.path import expanduser
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageStat

USER_HOME = expanduser("~")
USER_HOME_CONFIG_FILE = "{}/{}".format(USER_HOME, '.image_label_config.ini')

CONFIG = configparser.ConfigParser()

# top, top right, right, bottom right, etc
LOCATIONS = "T TR R BR B BL L TL".split()

# used to calc x and y coords
LOCS_TOP_OR_BOTTOM = ('T', 'B')
LOCS_LEFT_OR_RIGHT = ('L', 'R')
LOCS_TOP_EDGE = ('TL', 'T', 'TR')
LOCS_BOTTOM_EDGE = ('BL', 'B', 'BR')
LOCS_LEFT_EDGE = ('TL', 'L', 'BL')
LOCS_RIGHT_EDGE = ('TR', 'R', 'BR')

# RGB values
COLORS = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 153, 0),
    'yellow': (255, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}

ACCEPTABLE_COLORS = sorted(COLORS.keys())

# http://pillow.readthedocs.io/en/3.1.x/handbook/image-file-formats.html
OUTPUT_FORMATS = 'BMP JPEG PNG'.split()

PARSER = argparse.ArgumentParser(
    description='Add a text label to an existing image. '
                'Optionally, also rotate the image.',
    argument_default=argparse.SUPPRESS)

PARSER.add_argument('-S', '--setting',
                    type=str,
                    help='Name of section in config file to use.')
PARSER.add_argument('-T', '--label_text',
                    type=str,
                    help='Label text')
PARSER.add_argument('-L', '--label_location',
                    choices=LOCATIONS,
                    help='Location of the label on the image.')
PARSER.add_argument('-C', '--font_color',
                    choices=COLORS.keys(),
                    help='Font color of the label text.')
PARSER.add_argument('-F', '--font_file',
                    help='Path to TTF font file to use to generate the text label.')
PARSER.add_argument('-Z', '--font_size',
                    type=int,
                    help='Integer: Font size of the label text. This will be reduced as needed to ensure the text will fit within the picture and offsets.')
PARSER.add_argument('-H', '--label_offset_LR',
                    type=int,
                    help='Integer: Pixels to offset the label from the left '
                    'and right of the image.')
PARSER.add_argument('-V', '--label_offset_TB',
                    type=int,
                    help='Integer: Pixels to offset the label from the top '
                    'and bottom of the image.')
PARSER.add_argument('-R', '--rotate',
                    type=int,
                    help='Integer: Degrees to rotate image clockwise [1-359].')
PARSER.add_argument('-J', '--jpg_quality',
                    type=int,
                    help='Integer: JPG quality [1-95]. Default is 93. Larger '
                    'affects output file size but may not improve actual '
                    'quality. Quality cannot get better than the original image.')
PARSER.add_argument('-B', '--black_for_BW',
                    action='store_true',
                    help='Use black as text color for black and white images. '
                    'Default is white.')
PARSER.add_argument('-I', '--list_ini_sections',
                    action='store_true',
                    help='List the sections in your config file for convenience.')
PARSER.add_argument('-O', '--output_format',
                    choices=OUTPUT_FORMATS,
                    help='Output file format. Default is JPEG.')

ARGS, FILES = PARSER.parse_known_args()


def get_dict_from_namespace_object(args):
    """Unwrap the namespace object to pull out a dict of values"""
    return vars(args)


PARSED = get_dict_from_namespace_object(ARGS)

if 'IMAGE_LABEL_CONFIG' in os.environ:
    print('Reading config file from environment: IMAGE_LABEL_CONFIG')
    CONFIG.read(os.environ['IMAGE_LABEL_CONFIG'])
elif os.access(USER_HOME_CONFIG_FILE, os.R_OK):
    print('Reading config file from home directory')
    CONFIG.read(USER_HOME_CONFIG_FILE)
else:
    print('Could not find/read config file from env location or home directory')

if 'list_ini_sections' in PARSED:
    print(' '.join(sorted(CONFIG.sections())))
    sys.exit(0)


def options():
    """function object to host options attributies"""
    pass


# internal defaults
options.font_color = 'red'
options.font_file = './open-sans/OpenSans-Bold.ttf'
options.font_size = 100
options.label_location = 'TL'
options.label_offset_TB = 50
options.label_offset_LR = 50
options.label_text = 'LABEL TEXT'
options.rotate = None
options.jpg_quality = 93
options.black_for_BW = False
options.output_format = 'JPEG'


def load_settings_values(mydict):
    """update provided settings"""

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


if 'DEFAULTS' in CONFIG:
    load_settings_values(CONFIG['DEFAULTS'])

# if setting option provided via CLI, load that section's values
if 'setting' in PARSED:
    MYSECTION = PARSED['setting']
    if MYSECTION in CONFIG:
        load_settings_values(CONFIG[MYSECTION])
    else:
        print('ERROR: --setting value of {} is not included in the config'
              ' file'.format(MYSECTION))

# load any additional CLI options
load_settings_values(PARSED)

if options.font_color not in ACCEPTABLE_COLORS:
    print('Font color choice of {} is not among acceptable values of {}'
          .format(options.font_color, ACCEPTABLE_COLORS))
    sys.exit(1)

if options.label_location not in LOCATIONS:
    print('Location choice of {} is not among acceptable values of {}'
          .format(options.label_location, LOCATIONS))
    sys.exit(1)

if options.rotate:
    if not 0 < options.rotate < 360:
        print('ERROR: --rotate must be between 1-359 inclusive')
        sys.exit(1)

if not 1 <= options.jpg_quality <= 95:
    print('jgp_quality must be between 1-95. This will affect image quality '
          'and output jpg/jpeg file size')
    sys.exit(1)

if isinstance(options.black_for_BW, str):
    if options.black_for_BW == 'True':
        options.black_for_BW = True
    elif options.black_for_BW == 'False':
        options.black_for_BW = False
    else:
        print('ERROR: When setting black_for_BW via config file,'
              ' it must be set to True or False')
        sys.exit(1)

if options.output_format not in OUTPUT_FORMATS:
    print('ERROR: Output format {} is not valid, choose from {}'
          .format(options.output_format, OUTPUT_FORMATS))
    sys.exit(1)

TRUE_TYPE_FONT_MAGIC = b'\x00\x01\x00\x00'
with open(options.font_file, 'rb') as f:
    FIRST_FOUR_BYTES = f.read(4)
    if FIRST_FOUR_BYTES != TRUE_TYPE_FONT_MAGIC:
        print('The font file provided does not appear to be a True Type Font file')
        sys.exit(1)


# https://stackoverflow.com/questions/20068945/
# detect-if-image-is-color-grayscale-or-black-and-white-with-python-pil
def is_black_and_white(myimg):
    """Determine if image is black and white based on color variance"""

    # choosing 200 because I had some color images that only had ~500 variance
    color_variance_threshold = 200

    variance_tuple = ImageStat.Stat(myimg).var
    maxmin = abs(max(variance_tuple) - min(variance_tuple))

    if len(variance_tuple) == 1:
        # greyscale images only return a one-item tuple
        return True
    elif maxmin < color_variance_threshold:
        # otherwise you are guessing based on variance
        return True
    else:
        return False


def process_file(filename):
    """Make file modifications as needed and save"""

    img = Image.open(filename)

    if options.rotate:
        # rotation is ccw but can take negative numbers for cw, so multi input by -1
        # expand prevents truncation of image but can result in black borders
        img = img.rotate(int(options.rotate) * -1, expand=True)

    image_width, image_height = img.size
    draw = ImageDraw.Draw(img)


    def get_text_width_height(myfont):
        return draw.textsize(options.label_text, font=myfont)


    def get_font_that_fits(fontsize):
       
        myfont = ImageFont.truetype(options.font_file, int(fontsize))
        text_width, text_height = get_text_width_height(myfont)

        if options.label_offset_LR * 2 + text_width < image_width and \
           options.label_offset_TB * 2 + text_height < image_height:
            return myfont
        else:
            return get_font_that_fits(fontsize - 1)


    font = get_font_that_fits(options.font_size)
    text_width, text_height = get_text_width_height(font)

    # establish print location x
    if options.label_location in LOCS_LEFT_EDGE:
        x_coord = options.label_offset_LR
    elif options.label_location in LOCS_TOP_OR_BOTTOM:
        x_coord = (image_width - text_width) / 2
    elif options.label_location in LOCS_RIGHT_EDGE:
        x_coord = image_width - (text_width + options.label_offset_LR)

    # establish print location y
    if options.label_location in LOCS_TOP_EDGE:
        y_coord = options.label_offset_TB
    elif options.label_location in LOCS_LEFT_OR_RIGHT:
        y_coord = (image_height - text_height) / 2
    elif options.label_location in LOCS_BOTTOM_EDGE:
        y_coord = image_height - (text_height + options.label_offset_TB)

    if is_black_and_white(img):
        # when the image is black and white, draw.text needs a single color,
        # not a 3-tuple RGB color
        if options.black_for_BW:
            bwcolor = 0
            bwcolortext = 'black'
        else:
            bwcolor = 255
            bwcolortext = 'white'

        print('Image appears to be black and white, which cannot take RGB text'
              ', so using {} as text color'.format(bwcolortext))
        draw.text((x_coord, y_coord), options.label_text, bwcolor, font=font)
    else:
        draw.text((x_coord, y_coord),
                  options.label_text,
                  COLORS[options.font_color],
                  font=font)

    if '.' in os.path.basename(filename):
        # leave off the extension
        path, _ = os.path.splitext(filename)
    else:
        path = filename

    # add 'altered' to filename to prevent overwriting original
    outfilename = "{}.altered.{}".format(path, options.output_format.lower())

    # of BMP JPEG PNG only JPEG consumes the 'quality' parameter
    img.save(outfilename, format=options.output_format, quality=options.jpg_quality)


for filename in FILES:
    process_file(filename)
