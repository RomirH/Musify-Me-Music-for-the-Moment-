from speech_to_text import SpeechToText
from nlp import Keywords
from search import YouTubeAPI, SongQueue
from threading import Thread
from ibm_watson.websocket import RecognizeCallback



class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        # Opens up a new thread to process speech input and search for a video
        search_thread = Thread(target=handleSpeechInput, args=(transcript[0]['transcript'],))
        search_thread.start()

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))
        speech_to_text.restart()

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))



def handleSpeechInput(text):

    if "restart music listener" in text.lower():
        speech_to_text.restart()

    elif "start music listener" in text.lower():
        speech_to_text.start()

    elif "stop music listener" in text.lower():
        speech_to_text.stop()

    else :
        # Processes speech into emotions and keywords
        #kwds = keywords.getKeywords(text)
        #youtube.search(kwds)
        
        kwds = keywords.getKeywords(text)
        print(kwds)
        SQ.add_by_kw(kwds)
        SQ.play_first()
        print(SQ.queue)


###commented out prep for integration of SongQueue class###
#class MyRecognizeCallback(RecognizeCallback):
#    def __init__(self):
#        RecognizeCallback.__init__(self, squeue = SongQueue(api_key='AIzaSyCjgFgk2bdUS8cr74K9wiopWDdfXhwgt9g'))
#        self.squeue = squeue
#
#    def on_transcription(self, transcript):
#        # Opens up a new thread to process speech input and search for a video
#        search_thread = Thread(target=handleSpeechInput, args=(transcript[0]['transcript'],self.squeue))
#        search_thread.start()
#
#    def on_connected(self):
#        print('Connection was successful')
#
#    def on_error(self, error):
#        print('Error received: {}'.format(error))
#        speech_to_text.restart()
#
#    def on_inactivity_timeout(self, error):
#        print('Inactivity timeout: {}'.format(error))
#
#def handleSpeechInput(text, squeue):
#    if "restart music listener" in text.lower():
#        speech_to_text.restart()
#
#    elif "start music listener" in text.lower():
#        speech_to_text.start()
#
#    elif "stop music listener" in text.lower():
#        speech_to_text.stop()
#        squeue.clear()
#
#    else :
#        # Processes speech into emotions and keywords
#        kwds = keywords.getKeywords(text)
#        squeue.add_by_kw(kwds)




# Begin an instance of the NLP Keyword class
keywords = Keywords(api_key = 'I8V3ujhV1XG3VZDxV8sWc3wcD_CNdmdk4RYgJLP9x3Ne')


# Begin an instance of the SpeechToText class
speech_to_text = SpeechToText(api_key = '1gJQDKekWxkirik9EdSYTYRA42vd0UIk2aFONeAD-aYU', callback = MyRecognizeCallback())

# Begin an instance of the YouTubeAPI class
youtube = YouTubeAPI(api_key='AIzaSyCjgFgk2bdUS8cr74K9wiopWDdfXhwgt9g')
SQ = SongQueue(api_key='AIzaSyCjgFgk2bdUS8cr74K9wiopWDdfXhwgt9g', driver="chrome")
# Start recording and processing speech
speech_to_text.start()


