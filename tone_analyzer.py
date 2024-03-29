import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class ToneAnalyzer():
    def __init__(self,api_key):
        self.authenticator = IAMAuthenticator(api_key)
        self.tone_analyzer = ToneAnalyzerV3(version='2017-09-21', authenticator=self.authenticator)
    def analyze(self,sentence):
        return self.tone_analyzer.tone(sentence).get_result()

# import json
# from ibm_watson import ToneAnalyzerV3
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# class AnalyzeTone():
#     def __init__(self,s):
#         self.tones = {}
#         self.sentence = s
#         self.authenticator = IAMAuthenticator('3879mC57DARnUoMaGEXT8F0brMiI06nG2TzcBiBjeKR_')
#         self.tone_analyzer = ToneAnalyzerV3(
#             version='2017-09-21',
#             authenticator=self.authenticator
#         )
#         self.tone_analyzer.set_service_url("https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/eb91ab5d-f42d-4fb8-9a20-a4dd9c49ef1f")

        

#     def analyze(self):    
#         analysis = self.tone_analyzer.tone(
#             {'text':self.sentence},
#             content_type='application/json'
#         ).get_result()

#         # print(analysis['document_tone']['tones'][0])

#         try:
#             for each in analysis['sentences_tone']:
#                 t = each['tones']
#                 for i in t:
#                     if i['tone_name'] in self.tones:
#                         self.tones[i['tone_name']] += 1
#                     else:
#                         self.tones[i['tone_name']] = 1
#         except:
#             self.tones[analysis['document_tone']['tones'][0]['tone_name']] = 1
    
#     def result(self):
#         return [self.tones, max(self.tones, key=self.tones.get)]

# if __name__ == "__main__":
#     at = AnalyzeTone("I hope this works.")
#     at.analyze()
#     print(at.result())
