import urllib
import webbrowser
from googleapiclient.discovery import build
#pip install selenium and google-api-python-client

api_key = "AIzaSyCjgFgk2bdUS8cr74K9wiopWDdfXhwgt9g"

#browser that will start playing music
#need to put the executable path for this to open the browser, will be different in diff machines
webbrowser.register("chrome", None,
            webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome"))

# webbrowser.register("chrome", None,
#             webbrowser.BackgroundBrowser("C:\ProgramData\Microsoft\Windows\Start Menu\Programs"))

#request format
youtube = build("youtube", "v3", developerKey=api_key)

#search function
def search(keywords: list):
    #Parameters: Takes in a list of keywords
    #Return: Returns a json list which includes video url, length, id, etc

    #build query list based on keywords
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
    request = youtube.search().list(q=query_list, part="snippet",type="video")
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


#play with different keywords
search(["happy", "beats", "jcole"])
