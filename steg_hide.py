import os.path
import numpy as np
from PIL import Image

DEFAULT_IMAGE = "hidden.png"
DEFAULT_MESSAGE = "hello world!"


def checkImage(image):
    """
        this function receives an image
        and checks if it has 3 dimensions
    """
    if len(image.shape) != 3:
        return False
    else:
        return True


def checkText(text):
    """
        this function receives text
        and checks if its ascii
    """
    if text.isascii():
        return True
    else:
        return False


def checkPath(path):
    """
    this function receives an image path
    and checks if it exists
    """
    if os.path.exists(path):
        return True
    else:
        return False


def hide(array, imageName):
    """
        this is the hide function
        this function receives an array and the image name
        hide the text it receives from the user
        and sends it to the main function to be saved
    """
    # check again if the image exists and open the image for current use
    if checkPath(imageName):
        im = Image.open(imageName)
    userMessage = input("enter text to hide(Default in case of empty is hello world!):")
    if len(userMessage) == 0:
        userMessage = DEFAULT_MESSAGE
    if not checkText(userMessage):
        print("Unsupported text format, exiting\n")
        exit(-1)

    # convert to binary
    binaryText = ''.join(format(ord(i), '08b') for i in userMessage)
    # reshape the image array
    imgArr = array.flatten()
    dataLen = len(binaryText)
    if dataLen > len(imgArr):
        print("Text length is bigger then image length, not enough space. Will not encode the whole text\n")
    for i in range(len(imgArr)):
        if binaryText[i] == '1':
            val = imgArr[i]
            val = '{0:b}'.format(val)
            val = val[:-1] + '1'
            imgArr[i] = int(val, 2)
        elif binaryText[i] == '0':
            val = imgArr[i]
            val = '{0:b}'.format(val)
            val = val[:-1] + '0'
            imgArr[i] = int(val, 2)
        if i == len(binaryText) - 1:
            break

    # reshape the image array back to its original size
    try:
        returnArr = imgArr.reshape(im.size[1], im.size[0], -1)
    except:
        print("the image can't be reshape \n please try again with a different image")
        exit(-1)

    # create a new image and returns it
    hiddenImg = Image.fromarray(returnArr)
    return hiddenImg


def main():
    """
        this is the main function
        it checks the image received from the user
        calls the hide function
        and save the image after the return
    """
    # get an image from the user and checks its legit
    validImage = False
    while not validImage:
        imagePath = input("Please provide image to extract message from(Default in case of empty is hidden.png):\n")
        if len(imagePath) == 0:
            imagePath = DEFAULT_IMAGE
        if not checkPath(imagePath):
            print("Path to image is invalid")
        else:
            validImage = True
    # open the image and convert to numpy
    image = Image.open(imagePath)
    imageNP = np.array(image)
    if not checkImage(imageNP):
        print("Main: unsupported image type\n")
        exit(-1)

    hiddenIMG = hide(imageNP, imagePath)
    hiddenIMG.save('_' + imagePath)


if __name__ == '__main__':
    main()
