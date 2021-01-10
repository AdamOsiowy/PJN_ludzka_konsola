import speech_recognition as sr
import winsound


def recognizeVoice():
    r = sr.Recognizer()
    # print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=1)
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.record(source, duration=4)
    try:
        result = r.recognize_google(audio, language='pl-PL')
    except:
        result = ''
    emitSignalOnFinished()
    # print(f'recognize result: {result}')
    return result


def emitSignalOnFinished():
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
