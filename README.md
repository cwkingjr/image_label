# Image Label
Application to add a label to one or more images.

Optionally, the user may rotate the images and/or change the output file image format.

See README.config.md and image_label_config.ini for examples of how to set up a config file for preset options.

See help.output.txt for info on how to pass command line arguments.

See README.config.md for an explanation on how image-processing options/settings/arguments are prioritized from different locations (command line wins).

Example invocations:

    $image_label.py -h (outputs help info and exits)

    $image_label.py -I (lists the sections in your config file and exits)

    $image_label.py --label_text="TOP" --font_color=red --lable_offset_TB=5 --label_offset_LR=10 --font_size=16 --label_location=TL image1.jpg image2.jpg

    $image_label.py -T="TOP" -C=red -V=5 -H=10 -Z=16 -L=TL image1.jpg image2.jpg (same as above)

    $image_label.py --setting=top image1.jpg image2.jpg (uses config file [top] section values)

    $image_label.py image1.jpg image2.jpg (uses all default/DEFAULT settings)

    $image_label.py -O=PNG image1.jpg image2.jpg (uses all defaults, outputs in PNG format)

    $image_label.py -O=PNG -R=90 image1.jpg image2.jpg (same as above, but rotates image 90 degrees)