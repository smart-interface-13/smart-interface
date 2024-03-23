from vosk import Model, KaldiRecognizer
import pyaudio
import json

#model_path = "vosk-model-es-0.42"

class AudioTranscriber(object):

    def __init__(self, model_path : str, action_picker_text, 
                 action_picker_slides) -> None:
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.action_picker_text = action_picker_text
        self.action_picker_slides = action_picker_slides

    def open_channel(self):
        cap = pyaudio.PyAudio()
        stream = cap.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=16000, 
                        input=True, 
                        frames_per_buffer=8192)
        stream.start_stream()
        return stream
    
    def capture_voice(self, actions : dict, tool : str, ops : str):
        cap = pyaudio.PyAudio()
        stream = cap.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=16000, 
                        input=True, 
                        frames_per_buffer=8192)
        stream.start_stream()
        print("Start audio capture")
        
        while True:
            data = stream.read(8192)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                action = self._get_text_from_audio(result)
                action = self.action_picker_text.map_input_to_action(action, "voice")
                action_sequence = self.action_picker_text.get_action_sequence(action=action,
                                                                              actions=actions,
                                                                              tool=tool,
                                                                              ops=ops)
                self.action_picker_text.execute_action(action_sequence)
                
    def _get_text_from_audio(self, result) -> str:
        if result.get('text') :
            print("Texto transrito:", result['text'])
        return result["text"]

#voice = AudioTranscriber(model_path)
#stream = voice.open_channel()
#voice.capture_voice(stream)