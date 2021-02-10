import urllib
import webbrowser
from googleapiclient.discovery import build
#pip install selenium and google-api-python-client

class YouTubeAPI():

    def __init__(self,api_key):
        self.youtube = build("youtube", "v3", developerKey=api_key)
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome"))

    def search(self,keywords):
        #Parameters: Takes in a list of keywords
        #Return: Returns a json list which includes video url, length, id, etc

        #build query list based on keywords
        if not len(keywords):
            return
        query_list = ""
        list_length = len(keywords)
        counter = 0
        for element in keywords:
            query_list += element
            counter += 1
            if(counter < list_length):
                # + sign required to attach more elements
                query_list += "+"
            
        #build request
        request = self.youtube.search().list(q=query_list, part="snippet",type="video",videoCategoryId='10')
        response = request.execute()
        
        #print(response.items())
        #take a look at the json response

        #just as an example
        #'items' holds a list
        #grab first song and get it's video id
        first_song = response['items'][0]['id']['videoId']
        
        #build URL
        url = "https://www.youtube.com/watch?v=" + first_song
        webbrowser.get('chrome').open(url)
