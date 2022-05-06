import os

import speech_recognition as sr


def recognizeText(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        return text


def loadRealOutput():
    filename = './translations/trans1.txt'
    res = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            low = line.lower()
            res.append(low[:len(low)-1])
    return res


def loadComputedOutput():

    directory = 'dataset1'
    output = []
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            to_add = [f,recognizeText(f)]
            output.append(to_add)
    return output


#!/usr/bin/env python


def wer(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3

    3
    """
    # initialisation
    import numpy

    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]


def getError(realOut,computedOut):

    i = 0
    totalError = 0
    for elem in realOut:
        split = elem.split()
        realPhrase = split[1:]
        err = wer(realPhrase,computedOut[i][1].split())
        totalError = totalError + err
        i = i+1
    return totalError/len(realOut)




if __name__ == "__main__":
    import doctest

    doctest.testmod()





def main():


    filename = './dataset1/1272-141231-0000.flac'

if __name__ == "__main__":
    #main()
    modelErr = getError(loadRealOutput(),loadComputedOutput())
    print('Totla error:',modelErr)


