from vosk import Model, KaldiRecognizer
import pyaudio
import json

model_path = "vosk-model-es-0.42"

class AudioTranscriber(object):

    def __init__(self, model_path : str) -> None:
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def open_channel(self):
        cap = pyaudio.PyAudio()
        stream = cap.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=16000, 
                        input=True, 
                        frames_per_buffer=8192)
        stream.start_stream()
        return stream
    
    def capture_voice(self, stream):
        print("Start audio capture")
        while True:
            data = stream.read(4096)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                if result.get('text') :
                    print("Texto transrito:", result['text'])

voice = AudioTranscriber(model_path)
stream = voice.open_channel()
voice.capture_voice(stream)