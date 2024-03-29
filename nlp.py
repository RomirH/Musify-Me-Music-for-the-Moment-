import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions


class Keywords():
    def __init__(self,api_key):
        # Initialize connection to IBM Watson API
        self.authenticator = IAMAuthenticator(api_key)
        self.nlp = NaturalLanguageUnderstandingV1(
            version='2020-08-01',
            authenticator=self.authenticator
        )
    def getKeywords(self,text):
        try:
            # Raw data containing keywords and emotions of the input string
            response = self.nlp.analyze(
                text = text,
                features = Features(keywords=KeywordsOptions())
            ).get_result()
            
            # Initializing output list
            output = set()

            # Parsing data to return list of keywords/emotions
            for keyword in response['keywords']:
                if keyword["text"] == "HESITATION": continue
                output.add(keyword["text"])
            return list(output)

        except:
            return []

        