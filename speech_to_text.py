import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import AudioSource
from threading import Thread
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from queue import Queue, Full
import time

CHUNK = 1024
BUF_MAX_SIZE = CHUNK * 10

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class SpeechToText():
    def __init__(self,api_key,callback):
        # Initialize connection to IBM Watson API
        self.callback = callback
        self.authenticator = IAMAuthenticator(api_key)
        self.speech_to_text = SpeechToTextV1(authenticator=self.authenticator)
        self.status = 0
        
    def start(self):
        if self.status == 1:
            print("Audio capture already in progress.")
        else:
            self.status = 1
            self.queue = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))
            self.audio_source = AudioSource(self.queue, True, True)
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=self.pyaudio_callback,
                start=False
            )
            self.stream.start_stream()
            try:
                recognize_thread = Thread(target=self.recognize_using_weboscket, args=())
                recognize_thread.start()

                while self.status:
                    pass
            except KeyboardInterrupt:
                self.stop()

    def stop(self,restart=False):
        if self.status == 0:
            print("Audio capture not in progress.")
        else:
            if not restart : print("Audio capture terminating.")
            self.status = 0
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            self.audio_source.completed_recording()
    def restart(self):
        print("Restarting Audio Capture.")
        self.stop(restart = True)
        time.sleep(3)
        self.start()


    def pyaudio_callback(self, in_data, frame_count, time_info, status):
        try:
            self.queue.put(in_data)
        except Full:
            pass
        return (None, pyaudio.paContinue)

    def recognize_using_weboscket(self,*args):
        self.speech_to_text.recognize_using_websocket(
            audio=self.audio_source,
            content_type='audio/l16; rate=44100',
            recognize_callback=self.callback,
            interim_results=True,
            split_transcript_at_phrase_end=True,
            profanity_filter = False,
            speech_detector_sensitivity = 0.7
        )


        