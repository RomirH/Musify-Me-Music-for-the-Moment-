from tone_analyzer import ToneAnalyzer
from speech_to_text import SpeechToText
from threading import Thread
from ibm_watson.websocket import RecognizeCallback

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        sentiment_thread = Thread(target=analyze_tone, args=(transcript[0]['transcript'],))
        sentiment_thread.start()

def analyze_tone(sentence):
    print("\nSpeaker : ", sentence, "\nTones : ",tone_analyzer.analyze(sentence))

tone_analyzer = ToneAnalyzer(api_key = '3879mC57DARnUoMaGEXT8F0brMiI06nG2TzcBiBjeKR_')

speech_to_text = SpeechToText(api_key = '1gJQDKekWxkirik9EdSYTYRA42vd0UIk2aFONeAD-aYU',callback = MyRecognizeCallback())

speech_to_text.start()