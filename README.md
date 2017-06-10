# Image Label
Application to add a label to one or more images.

This is a project based on talking to a cell tower inspector (Josh) that has to routinely add one label from a preset list of labels to tower inspection pictures (TOP, BOTTOM, etc). This project is an effort to see if I can put together an application that makes this job easier/faster that is very intuitve to use.

Moving forward, these are my assumptions:

- Must be able to run on Windows 10
- Must provide extensive install instructions
- Should have configs for default settings
- Should allow non-software-technical user to add/change configs
- Should allow command-line override of default configs
- Should allow adding the same label to one or more images per invocation
- Must retain the original image files (not overwrite)

Settings should cover these items:

- True Type Font file location
- Font size (12, 14, 16, etc)
- Text (what text to insert)
- Text location on image based on top, right, bottom, left (T, TR, R, BR, B, BL, L, TL)
- Text offset for top and bottom (pixels from edge)
- Text offset for left and right (pixels from edge)
- Text color

Things that may need to be considered / added later:

- Calculating size and point of the label based on size and resolution of the original image
- Providing frozen windows binary to ease installation
- Image output format

The idea is that a user would be able to invoke something like this on the command line:

    $image_label --text="TOP" --color=red --offset_TB=5 --offset_LR=10 --size=16 --location=TL image1.jpg image2.jpg

    $image_label --setting=top image1.jpg image2.jpg (uses defaults and [top] setting overrides)

    $image_label image1.jpg image2.jpg (uses all default settings)