This is a project based on talking to a cell tower inspector (Josh) that has to routinely add one label from a preset list of labels to tower inspection pictures (TOP, BOTTOM, etc). This project is an effort to see if I can put together an application that makes this job easier/faster that is very intuitve to use.

Moving forward, these are my assumptions:

- Must be able to run on Windows 10
- Must provide clear/complete install instructions
- Should have configs for default settings
- Should allow non-software-technical user to add/change configs
- Should allow command-line override of default configs
- Should allow adding the same label to one or more images per invocation
- Must retain the original image files (not overwrite)
- Should allow changing the output file format

Settings should cover these items:

- True Type Font file location
- Font size (12, 14, 16, etc)
- Font color (red, green, blue, white, black, yellow)
- Label text (what text to insert)
- Label location on image based on top, right, bottom, left (T, TR, R, BR, B, BL, L, TL)
- Label offset for top and bottom (pixels from edge)
- Label offset for left and right (pixels from edge)

Things that may need to be considered / added later:

- Providing frozen windows binary to ease installation