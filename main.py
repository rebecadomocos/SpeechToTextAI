import os


import speech_recognition as sr
from google_trans_new import google_translator
from gtts import gTTS



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


def dialog():
    phrases_number_to_consider = 22
    speaker1_dataset_prefix = "dataset1/1272-141231-00"
    speaker2_dataset_prefix = "dataset2/Recording"
    spoken_fileName = "./spoken/current.mp3"
    translator = google_translator()
    for i in range(1,phrases_number_to_consider):

        speaker1_filenameString = ""
        speaker2_filenameString = ""
        if i >= 10:
            speaker1_filenameString = speaker1_dataset_prefix + str(i) + ".flac"
        else:
            speaker1_filenameString = speaker1_dataset_prefix + "0" + str(i) + ".flac"

        speaker2_filenameString = speaker2_dataset_prefix + str(i) + ".flac"
        # speaker one
        text_eng = recognizeText(speaker1_filenameString)
        print("*************************************************************")
        print("Speaker 1(EN):"+text_eng)
        translation = translator.translate(text_eng, lang_tgt='ro')
        print("Speaker 1(RO):" + translation)


        myobj = gTTS(text=translation, lang='ro', slow=False)

        myobj.save(spoken_fileName)
        # here it should speak the spoken_fileName
        #speaker two
        text_ro = recognizeTextRO(speaker2_filenameString)
        print("Speaker 2(RO):"+text_ro)
        translation = translator.translate(text_ro,lang_tgt='en')
        print("Speaker 2(EN):" + translation)
        myobj = gTTS(text=translation, lang='en', slow=False)
        myobj.save(spoken_fileName)
        # here it should speak the spoken_fileName

        print("*************************************************************")


if __name__ == "__main__":

    dialog()
