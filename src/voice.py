import speech_recognition as sr
import winsound


def recognizeVoice():
    r = sr.Recognizer()
    # print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=1)
    with mic as source:
        audio = r.listen(source)
    result = r.recognize_google(audio, language='pl-PL')
    emitSignalOnFinished()
    return result


def emitSignalOnFinished():
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
