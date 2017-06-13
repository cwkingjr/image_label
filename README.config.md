# Configuration File Defaults / Setting Options

These are the internal default configuration settings that will be used if nothing is provided via the config file DEFAULTS section, the section chosen in the configuration file via the --setting option, or any options chosen via the command line options. Option priority is: command line (first), config file section via --setting (second), config file DEFAULTS section (third), and internal defaults (last).

- label_text = "Default Insertion Text"
- label_color = "red" # picked from list below
- font_size = 100 # size the text will be printed
- label_offset_LR = 50 # font points from edge of left and right of image
- label_offset_TB = 50 # font points from edge of top and bottom of image
- label_location = "TL" # Top Left of image
- font_file = "./open-sans/OpenSans-Bold.ttf" # path to your ttf font file

The settings value choices are:

- color: red, blue, green, yellow, white, black
- location: T, TR, R, BR, B, BL, L, TL

To override one or more of these settings, add a new unique configuration section to your config file, like this:

```
[top]
lable_text = TOWER TOP

[bottom]
lable_text = TOWER BOTTOM
lable_location = BL

[left]
label_text = Some image that needs a left side label
font_color = blue
label_location = L

[whatever]
label_text = NORTH -->
label_location = BR
