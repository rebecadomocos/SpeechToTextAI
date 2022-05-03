import speech_recognition as sr
import pyttsx3


def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def main():
    r = sr.Recognizer()
    with sr.Microphone() as source2:
        r.adjust_for_ambient_noise(source2, duration=0.2)
        print("say smth")
        # listens for the user's input
        audio2 = r.listen(source2, phrase_time_limit=2)

        # Using google to recognize audio
        MyText = r.recognize_google(audio2)
        #MyText = MyText.lower()

        print("Did you say " + MyText)
        # r.adjust_for_ambient_noise(source, duration=0.2)
        #
        # print("Say something...")
        # audio = r.listen(source)
        # print("here")
        # try:
        #     print('You have said : \n' + r.recognize_google(audio))
        #
        # except Exception as e:
        #     print("Error" + str(e))
    filename = './dataset1/1272-141231-0000.flac'
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)
    # while (1):
    #
    #     # Exception handling to handle
    #     # exceptions at the runtime
    #     try:
    #
    #         # use the microphone as source for input.
    #         with sr.Microphone() as source2:
    #
    #             # wait for a second to let the recognizer
    #             # adjust the energy threshold based on
    #             # the surrounding noise level
    #             r.adjust_for_ambient_noise(source2, duration=0.2)
    #
    #             # listens for the user's input
    #             audio2 = r.listen(source2)
    #
    #             # Using google to recognize audio
    #             MyText = r.recognize_google(audio2)
    #             MyText = MyText.lower()
    #
    #             print("Did you say " + MyText)
    #             SpeakText(MyText)
    #
    #     except sr.RequestError as e:
    #         print("Could not request results; {0}".format(e))
    #
    #     except sr.UnknownValueError:
    #         print("unknown error occured")


if __name__ == "__main__":
    main()
