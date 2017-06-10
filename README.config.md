# Configuration File Defaults / Setting Options

These are the default configuration settings that will be used if nothing is provided via the option chosen in the configuration file or via the command line options.

text = "Default Insertion Text"
color = "red" # picked from list below
size = 150 # size the text will be printed
offset = 50 # font points from edge of image
location = "NW" # compass direction, e.g., top left is NW, bottom right is SE
font_file = "./open-sans/OpenSans-Bold.ttf" # path to your ttf font file

The settings value choices are:

color: red, blue, green, yellow, white, black
location: N, NE, E, SE, S, SW, W, NW

To override one or more of these settings, add a new unique configuration section to your config file, like this (settings not provided use the default):

```
[left]
text = "LEFT"
color = "blue"
location = "W"

[right]
text = "RIGHT"
location = "E"
