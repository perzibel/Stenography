import os
import time
import sys
from PIL import Image
import numpy as np

SPECIAL_CHARS = [32, 33, 44, 46, 63]  # special characters int values to remember
THREE = 3  # number of dimensions and a number for RGB
BYTE = 8  # number of byte in a char
DEFAULT_IMAGE_PATH = "hidden.png"  # default image name
EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')  # extension for images
ID_FILE = "result.txt"  # the file name to print
SPACE = " "  # saved as string and not as int value
DOT = "."  # saved as string and not as int value


def checkDictionary(word: str, dictionary, wordList):
    """
      this function checks if a given word
      is in a given dictionary
      """
    if len(word) == 0:
        return False
    wordToFind = word[0].lower() + word[1:]
    wordToFind.strip()
    for wordInD in dictionary:
        if wordToFind == wordInD:
            if len(wordList) > 1:
                if wordList[len(wordList) - 1] == SPACE and wordToFind != wordList[len(wordList) - 2].lower():
                    return True
                return False
            return True
    return False


def checkPath(path):
    """
      this function checks to see if a path is valid
      """
    if os.path.exists(path) and path.lower().endswith(EXTENSIONS):
        return True
    return False


def extractBinArray(tup, lsb1, lsb2, lsb3):
    """
      this function extract the binary array
      into 3 new arrays of each least significant bit
      by position
      """
    for i in tup:
        for x in range(THREE):  # disregarding A in RGBA (incase exists)
            lsb1.append(i[x] & 1)  # lsb
            lsb2.append(int((i[x] & 2) / 2))  # second from the end lsb
            lsb3.append(int((i[x] & 4) / 4))  # third from the end lsb


def isAscii(byteArray):
    """
      this function checks if a given byte array is an ascii character
    """
    # Convert the byte array to a string of binary characters
    byteString = ''.join(map(str, byteArray))
    # Convert the binary string to an integer
    byteInt = int(byteString, 2)
    # Check if the integer is within the ASCII range (0-127)
    if 65 <= byteInt <= 90 or 97 <= byteInt <= 122:
        return True
    return False


def extractWord(arrayList, dictionary, index, wordList):
    """
      this function is for words extraction
      it converts a binary array into an integer
      and checks if it exists in the dictionary
    """
    word = ""
    returnTuple = []
    z = index + BYTE
    # Convert the byte array to a string of binary characters
    byteString = ''.join(map(str, arrayList[index:index + BYTE]))
    # Convert the binary string to an integer
    byteInt = int(byteString, 2)
    word += chr(byteInt)
    while isAscii(arrayList[z:z + 8]):
        byteString = ''.join(map(str, arrayList[z:z + BYTE]))
        # Convert the binary string to an integer
        byteInt = int(byteString, 2)
        word += chr(byteInt)
        z += 8
    # Check if in dictionary
    if checkDictionary(word, dictionary, wordList):
        returnTuple.append(z)
        returnTuple.append(word)
        return returnTuple
    elif len(word) > 3 and checkDictionary(word[:-1], dictionary, wordList):
        returnTuple.append(z - 8)
        returnTuple.append(word[:-1])
        return returnTuple
    returnTuple.append(index)
    return returnTuple


def extractDelimiter(lsb1, lsb2, lsb3, index):
    """
      this function extract the delimiter
      it converts a binary array into an integer
      and check if its a delimiter
    """
    # taking the next char from arrays to check if they are delimiters
    lsb1ByteString = ''.join(map(str, lsb1[index:index + BYTE]))
    lsb2ByteString = ''.join(map(str, lsb2[index:index + BYTE]))
    lsb3ByteString = ''.join(map(str, lsb3[index:index + BYTE]))
    # Convert the binary string to an integer
    lsb1Int = int(lsb1ByteString, 2)
    lsb2Int = int(lsb2ByteString, 2)
    lsb3Int = int(lsb3ByteString, 2)
    if SPECIAL_CHARS.count(lsb1Int) == 1:
        return chr(lsb1Int)
    elif SPECIAL_CHARS.count(lsb2Int) == 1:
        return chr(lsb2Int)
    elif SPECIAL_CHARS.count(lsb3Int) == 1:
        return chr(lsb3Int)
    else:
        return None


def checkContinuedDelimiter(wordList, delimiter):
    """
      this function checks for a delimiter
      to continue or stop
    """
    lIndex = len(wordList) - 1
    beforeSpace = (".", ",", "?", "!")
    if delimiter == SPACE and beforeSpace.count(wordList[lIndex]):
        return True
    if delimiter == DOT and wordList[lIndex] == DOT:
        return True
    return False


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    this function create a progress bar
    the decoding takes some time so i created a a progress bar
    to keep track and show where we are in the progress
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def decode(NParr: np.array):
    """
        this is the "main" function of the code
        it leads the decoding process and contains
        all the actions and function calls.

        this is where the magic happens!
    """
    print("the decryption is starting, please hold on ---")
    lsb1 = []
    lsb2 = []
    lsb3 = []
    wordList = []
    finalWordList = []
    i = 0
    counter = 0
    if len(NParr.shape) < THREE:
        print("Image is not with RGB color code (i.e., grayscale) and thus we cannot hide the text")
        exit(-1)
    with open('dictionary.txt') as f:
        dictionary = f.read().splitlines()

    # extract array
    for val in NParr:
        tempArray = []
        counter = 1
        for c in val:
            tempArray.append(c)
            if counter % THREE == 0:
                extractBinArray(tempArray, lsb1, lsb2, lsb3)
                tempArray = []
            counter += 1

    """
        looking for the words and printing the progress bar
    """
    printProgressBar(0, len(lsb1), prefix='Progress:', suffix='Complete', length=100)
    while i < len(lsb1) - BYTE:  # add word counter here
        printProgressBar(i, len(lsb1), prefix='Progress:', suffix='Complete', length=100)
        if counter == 0 and i != 0:
            z = 0
            for word in wordList:
                z += len(word)
            if len(wordList) < 4 or z < 5:
                wordList.clear()
                i -= z
            else:
                finalWordList.append(wordList)
                wordList = []

        if isAscii(lsb1[i:i + BYTE]):
            result = extractWord(lsb1, dictionary, i, wordList)
            if len(result) != 1:
                delimiter = extractDelimiter(lsb1, lsb2, lsb3, result[0])
                if delimiter is not None:
                    counter += 1
                    wordList.append(result[1])
                    wordList.append(delimiter)
                    i = result[0] + BYTE
                    continue
        if isAscii(lsb2[i:i + BYTE]):
            result = extractWord(lsb2, dictionary, i, wordList)
            if len(result) != 1:
                delimiter = extractDelimiter(lsb1, lsb2, lsb3, result[0])
                if delimiter is not None:
                    counter += 1
                    wordList.append(result[1])
                    wordList.append(delimiter)
                    i = result[0] + BYTE
                    continue
        if isAscii(lsb3[i:i + BYTE]):
            result = extractWord(lsb3, dictionary, i, wordList)
            if len(result) != 1:
                delimiter = extractDelimiter(lsb1, lsb2, lsb3, result[0])
                if delimiter is not None:
                    counter += 1
                    wordList.append(result[1])
                    wordList.append(delimiter)
                    i = result[0] + BYTE
                    continue
        if len(wordList) != 0:
            delimiter = extractDelimiter(lsb1, lsb2, lsb3,
                                         i)  # delimiter == ' ' and wordList[len(wordList) - 1] != delimiter
            # checking if there is a delimiter and it is
            if delimiter is not None and checkContinuedDelimiter(wordList, delimiter):
                wordList.append(delimiter)
                i += BYTE
                continue
        counter = 0
        i += 1
    """
        print the words found and writes the result into 
        the result file
    """
    f = open(ID_FILE, "a")
    for option in finalWordList:
        print(''.join(map(str, option)))
        f.write(''.join(map(str, option)))
    f.close()


def main():
    """
        the main function:
        1. ask for the input
        2. call the decode function
    """
    isValid = False
    while not isValid:
        imagePath = input("Please provide image to extract message from(Default in case of empty is hidden.png):\n")
        if len(imagePath) == 0:
            imagePath = DEFAULT_IMAGE_PATH
        if not checkPath(imagePath):
            print("Path to image is invalid")
        else:
            isValid = True
    image = Image.open(imagePath)
    data = np.array(image)
    decode(data)


if __name__ == '__main__':
    main()
