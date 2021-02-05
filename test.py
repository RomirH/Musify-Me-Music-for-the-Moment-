import json
import pandas as pd
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('3879mC57DARnUoMaGEXT8F0brMiI06nG2TzcBiBjeKR_')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)
tone_analyzer.set_service_url("https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/eb91ab5d-f42d-4fb8-9a20-a4dd9c49ef1f")

text = "What the fuck is going on! Why doesn't this work! I'm so upset right now that this is happening. What the fuck man? Ok how do we fix this?"

analysis = tone_analyzer.tone(
    {'text':text},
    content_type='application/json'
).get_result()

# tone = json.dumps(analysis, indent=2)

tones = {}
for each in analysis['sentences_tone']:
    t = each['tones']
    print(each['text'])
    print(t)
    for i in t:
        if i['tone_name'] in tones:
            tones[i['tone_name']] += 1
        else:
            tones[i['tone_name']] = 1

print(tones)

