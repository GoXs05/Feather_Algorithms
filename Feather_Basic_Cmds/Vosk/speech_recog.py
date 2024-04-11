from vosk import Model, KaldiRecognizer
import pyaudio

samplerate = 16000

model = Model(lang="en-us")
recognizer = KaldiRecognizer(model, samplerate)

mic = pyaudio.PyAudio()

listening = False

def listen():
    listening = True
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=samplerate, input=True, frames_per_buffer=8192)
    while listening:
        stream.start_stream()
        try:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                response = result[14:-3]
                listening = False
                stream.close()
                return response
        except OSError:
            pass