import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

class SpeechToText():

    def __init__(self,chunk = 1024, api_key = '1gJQDKekWxkirik9EdSYTYRA42vd0UIk2aFONeAD-aYU'):
        self.CHUNK = chunk
        self.BUF_MAX_SIZE = self.CHUNK * 10
        self.q = Queue(maxsize=int(round(self.BUF_MAX_SIZE / self.CHUNK)))
        self.audio_source = AudioSource(self.q, True, True)
        self.authenticator = IAMAuthenticator(api_key)
        self.speech_to_text = SpeechToTextV1(authenticator=self.authenticator)
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.audio = pyaudio.PyAudio()
        print("starting stream")
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.pyaudio_callback,
            start=False
        )
        self.stream.start_stream()
        try:
            recognize_thread = Thread(target=self.recognize_using_weboscket, args=())
            recognize_thread.start()
            while True:
                pass
        except KeyboardInterrupt:
            # stop recording
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            self.audio_source.completed_recording()

    def recognize_using_weboscket(self,*args):
        mycallback = MyRecognizeCallback()
        self.speech_to_text.recognize_using_websocket(audio=self.audio_source,
                                                content_type='audio/l16; rate=44100',
                                                recognize_callback=mycallback,
                                                interim_results=True,
                                                split_transcript_at_phrase_end=True,
                                                profanity_filter = False)
    def pyaudio_callback(self, in_data, frame_count, time_info, status):
        try:
            self.q.put(in_data)
        except Full:
            pass # discard
        return (None, pyaudio.paContinue)

# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)

    def on_close(self):
        print("Connection closed")

