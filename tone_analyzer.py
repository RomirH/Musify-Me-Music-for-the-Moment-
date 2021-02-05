import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class ToneAnalyzer():
    def __init__(self,api_key):
        self.authenticator = IAMAuthenticator(api_key)
        self.tone_analyzer = ToneAnalyzerV3(version='2017-09-21', authenticator=self.authenticator)
    def analyze(self,sentence):
        return self.tone_analyzer.tone(sentence).get_result()
