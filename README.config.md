# Configuration File Defaults / Setting Options

These are the default configuration settings that will be used if nothing is provided via the option chosen in the configuration file or via the command line options.

- text = "Default Insertion Text"
- color = "red" # picked from list below
- size = 150 # size the text will be printed
- offset_LR = 50 # font points from edge of left and right of image
- offset_TB = 50 # font points from edge of top and bottom of image
- location = "TL" # Top Left of image
- font_file = "./open-sans/OpenSans-Bold.ttf" # path to your ttf font file

The settings value choices are:

- color: red, blue, green, yellow, white, black
- location: T, TR, R, BR, B, BL, L, TL

To override one or more of these settings, add a new unique configuration section to your config file, like this (settings not provided use the default):

```
[top]
text = "TOWER TOP"

[bottom]
text = "TOWER BOTTOM"
location = "BL"

[left]
text = "Some image that needs a left side label"
color = "blue"
location = "L"

[right]
text = "NORTH -->"
location = "BR"
