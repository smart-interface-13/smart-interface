from vosk import Model, KaldiRecognizer
import pyaudio
import json
from src.utils import GestureLogger

logger = GestureLogger("logger1")

#model_path = "vosk-model-es-0.42"

class AudioTranscriber(object):
    """This class manages the microphone to process audio
    """

    def __init__(self, model_path : str, action_picker_text) -> None:
        """Inits the class

        Args:
            model_path (str): Path of the vosk model to use for STT
            action_picker_text (_type_): The picker of actions to map in the software
        """
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.action_picker = action_picker_text

    def open_channel(self):
        """Opens the audio channel to receive the data
        """
        cap = pyaudio.PyAudio()
        stream = cap.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=16000, 
                        input=True, 
                        frames_per_buffer=8192)
        stream.start_stream()
        return stream
    
    def capture_voice(self, actions : dict, tool : str, ops : str) -> str:
        """Captures the voice command and gets the action to trigger in the software
        Args:
            actions (dict): Supported actions by command
            tool (str): The current tool (text or slides)
            ops (str): Operative system

        Returns:
            str: a control message
        """
        cap = pyaudio.PyAudio()
        stream = cap.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=16000, 
                        input=True, 
                        frames_per_buffer=8192)
        stream.start_stream()
        logger.info("Start audio capture")
        
        while True:
            data = stream.read(8192)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                action = self._get_text_from_audio(result)
                action = self.action_picker.map_input_to_action(action, "voice")
                action_sequence = self.action_picker.get_action_sequence(action=action,
                                                                            actions=actions,
                                                                            tool=tool,
                                                                            ops=ops)
                out = self.action_picker.execute_action(action_sequence)
                if out == "close":
                    logger.info("Saliendo de modo comandos de voz")
                    return "gesture_mode"
                elif out == "exit":
                    return out
                
    def _get_text_from_audio(self, result) -> str:
        """Gets the transcription of the audio

        Args:
            result (_type_): Audio

        Returns:
            str: Transcription
        """
        if result.get('text') :
            text = result['text']
            logger.info(f"Texto transrito: {text}")
        return result["text"]