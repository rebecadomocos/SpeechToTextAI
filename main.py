import os

import six
from googletrans import Translator
import speech_recognition as sr
from pythonTranslateMain.google.cloud.translate_v2.client import Client
from gtts import gTTS
from playsound import playsound


def recognizeText(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        return text


def recognizeTextRO(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data,language='ro')
        return text

def loadRealOutput(translations):

    res = []
    with open(translations, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            low = line.lower()
            res.append(low[:len(low)-1])
    return res


def loadComputedOutput(directory):


    output = []
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            recognized = ""
            if directory == 'dataset1':
                to_add = [f,recognizeText(f)]
            else:
                to_add = [f, recognizeTextRO(f)]
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

    # modelErr = getError(loadRealOutput('./translations/trans1.txt'), loadComputedOutput('dataset1'))
    # print('En-error:',modelErr)
    # print()
    # modelErrRO = getError(loadRealOutput('./translations/Recording.trans.txt'), loadComputedOutput('dataset2'))
    # print('RO-error',modelErrRO)

    text_eng = recognizeText("dataset1/1272-141231-0005.flac")
    print(text_eng)
    translator = Translator()
    translation = translator.translate(text_eng, dest='ro', src='en')
    print(translation.text)

    language = 'ro'
    file = "./spoken/welcomeRO.mp3"
    myobj = gTTS(text=translation.text, lang=language, slow=False)
    myobj.save(file)
    playsound(file)

    text_ro = recognizeTextRO("dataset2/Recording1.flac")
    print(text_ro)
    translator2 = Translator()
    translation_ro = translator2.translate(text_ro, dest='en', src='ro')
    print(translation_ro.text)

    language = 'en'
    file = "./spoken/welcomeENG.mp3"
    myobj_ro = gTTS(text=translation_ro.text, lang=language, slow=False)
    myobj_ro.save(file)
    playsound(file)




