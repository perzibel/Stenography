# Libraries 
This code relies on the Numpy and PIL libraries for its implementation.

# Install
To install the required packages, follow these steps:

Open the command prompt or terminal.

Execute the following command to install the Numpy package:  python -m pip install numpy

Next, install the Pillow package by executing the following command:  python -m pip install Pillow

These commands will download and install the Numpy and Pillow packages necessary for the code to run successfully.

# Run
To execute any of the codes, simply use the following commands:

For steg_hide.py:
python steg_hide.py

For steg_decode.py:
python steg_decode.py

Running the respective command will initiate the program and execute the desired code.

# Hide
To hide a text in a PNG image, you need to provide an image path and a text of your choice as input in the command-line interface (CLI) when prompted.
The resulting image will be saved with the image name prefixed by an underscore ( _ ).

For example, if the original image is named "hidden.png," the resulting image will be saved as "_hidden.png."

# Decode
To decode the hidden text from an image, provide the path of the image containing the hidden text in the command-line interface (CLI).
Additionally, ensure that you have a dictionary containing the words you expect to find in the image.
Once the input is provided, the decoding process will commence.

During the decoding process, a progress bar will be displayed, indicating the progress of the operation.
Please note that the duration of the decoding process may vary based on the size of the dictionary used.
A larger dictionary may result in a longer decoding time.
