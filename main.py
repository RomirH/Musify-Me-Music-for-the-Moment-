from speech_to_text import SpeechToText
from nlp import NLP
from threading import Thread
from ibm_watson.websocket import RecognizeCallback

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        # Opens up a new thread to process speech input
        nlp_thread = Thread(target=getKeywordsAndEmotion, args=(transcript[0]['transcript'],))
        nlp_thread.start()

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

def getKeywordsAndEmotion(text):
    # Processes, Prints and Returns the keywords and dominating emotions of the speech input
    keywords = nlp.process(text)

    for kw in keywords:

        print( 
            "\nKeyword :",kw[0],
            "\nEmotion :",kw[1]
        )

    return keywords

# Begin an instance of the NLP Class
nlp = NLP(api_key = 'I8V3ujhV1XG3VZDxV8sWc3wcD_CNdmdk4RYgJLP9x3Ne')

# Begin an instance of the SpeechToText class
speech_to_text = SpeechToText(api_key = '1gJQDKekWxkirik9EdSYTYRA42vd0UIk2aFONeAD-aYU', callback = MyRecognizeCallback())

# Start recording and processing speech
speech_to_text.start()