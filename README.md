# Libraries 

this code uses Numpy and PIL libraries.

# Install
to install the packeges use:

1. python pip install numpy

2. python pip install Pillow 

# Run
to run any of the codes just use python steg_hide.py\ steg_decode.py
and the program will start.

# Hide
to hide a text in a png theres first needs to be a Image.

add an image path you'd like to use to the CLI when asked.

then add a text of your chosing.

the result will be saved as the image name starting with an underscore ( _ )
example: hidden.png ------> _hidden.png

# Decode
to decode enter an image with hidden text in it path to the CLI.

make sure you have a dictionery with the words you'r expecting to find in the image.

then just wait.

a progress bar will be shown letting you know of the progress (the bigger the dictionery -> the long the wait)
