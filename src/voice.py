import speech_recognition as sr
import winsound


def recognizeVoice(recognizer, audio):
    try:
        result = recognizer.recognize_google(audio, language='pl-PL')
        return result
    except LookupError:
        return ''


def startRecording():
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
    global stop_listening
    stop_listening = r.listen_in_background(m, recognizeVoice)


def stopRecording():
    global stop_listening
    stop_listening()
    emitSignalOnFinished()


def emitSignalOnFinished():
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
