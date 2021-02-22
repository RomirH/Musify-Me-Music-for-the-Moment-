import urllib
import webbrowser #for webbrowsing
from selenium import webdriver #for webbrowsing
from selenium.webdriver.common.keys import Keys #for sending commands to YouTube
from googleapiclient.discovery import build #for YouTube API
import time #for testing
import sys #for printing errors and exit codes
from threading import Lock #for thread locks
import urllib.request as urllib2
import http.cookiejar as cookielib
import json
import time
#pip install selenium and google-api-python-client

class YouTubeAPI():

    def __init__(self,api_key):
        self.youtube = build("youtube", "v3", developerKey=api_key)
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome"))

    def file_get_contents(url):
        url = str(url).replace(" ", "+") # just in case, no space in url
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        try:
            page = urllib2.urlopen(req)
            return page.read()
        except urllib2.HTTPError as e:
            print(e.fp.read())
        return ''

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
        request = self.youtube.search().list(q=query_list, part="contentDetails",type="video",videoCategoryId='10')
        response = request.execute()
        
        print(response.items())
        #take a look at the json response

        #just as an example
        #'items' holds a list
        #grab first song and get it's video id
        first_song = response['items'][0]['id']['videoId']
        
        #build URL
        url = "https://www.youtube.com/watch?v=" + first_song
        webbrowser.get('chrome').open(url)

class SongQueue():
    def __init__(self,api_key, driver='chrome'):
        """Creates a SongQueue.  Args: YouTube-api-key, driver(optional)"""
        #currently the only supported method of search is Youtube
        self.req_format = build("youtube", "v3", developerKey=api_key)  
        self.queue=[]      #listofurls
        self.tabs = []
        self.url_base = "https://www.youtube.com/watch?v="
        self.qlock = Lock() #queue lock
        self.tablock = Lock()

           
        if (driver != 'firefox') and (driver !='chrome'): 
            sys.stderr.write('SongQueue: supported drivers are \'chrome\' and \'firefox\'')
            sys.exit(-1)  
        self.driver = driver
        #if you're having driver issues, see SongQueue.play_first


    def __del__(self):
        #avoid leaving sockets hanging?
        #self.req_format.close()
        sys.stdout.write('deleted SongQueue.\n')

    def show_queue(self):
        return self.queue

    def add_by_kw(self, keywords: list, raw_num_to_add = 2):
        """queries YouTube based on kw and adds to list.  Args: ListOfKeywords, #songs-to-add(optional)"""
        #default length of songs to add is 5
        #Return: Returns the length of 

        try: 
            num_to_add = abs(int(raw_num_to_add))
        except:
            sys.stderr.write('SongQueue.add_by_kw: invalid number of songs to add')
            return

        if not len(keywords) > 0:
            sys.stderr.write('SongQueue.add_by_kw: no keywords provided')
            return

        LENGTH = 10 #placeholder for length
        #build query list based on keywords
        query_list = "music"  #search music by inputting music into query
        list_length = len(keywords)
        counter = 0
        for element in keywords:
            query_list += element
            counter += 1
            if(counter < list_length):
                # + sign required to attach more elements
                query_list += "+"
            
        #build request
        request = self.req_format.search().list(q=query_list,     #terms to query
                                                part="snippet",    #returns also description of vid
                                                type="video",       #searches only videos
                                                videoCategoryId='10', #searches music videos (?)
                                                videoDuration = 'medium') #between 4 and 20 mins
                                                
                                                #relatedToVideoId = -------
                                                #returned results will be related to the id input
                                                #could be used to find new songs
        
        response = request.execute() #send request
        
        #print(response.items())
        #take a look at the json response


        #for more info about the response
        #  https://developers.google.com/youtube/v3/docs/search#resource for individual songs
        #  https://developers.google.com/youtube/v3/docs/search/list for the list returned

        #adds urls of first num_to_add songs to the queue
        with self.qlock:
            for i in range(num_to_add):
                song = response['items'][i]
                #get song details -> length
                details = YouTubeAPI.file_get_contents("https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id=" + song['id']['videoId'] + "&key=AIzaSyCjgFgk2bdUS8cr74K9wiopWDdfXhwgt9g")
                #load json bytes
                translate = json.loads(details)
                duration = translate['items'][0]['contentDetails']['duration']
                #transform ISO-8601 to seconds
                try:
                    minutes = int(duration[2:4])
                except:
                    minutes = int(duration[2])
                try:
                    seconds = int(duration[-3:-1])
                except:
                    seconds = int(duration[-2])
                LENGTH = 60*minutes + seconds
                self.queue.append((self.url_base + song['id']['videoId'], LENGTH))
                

    def play(self):  
        """plays opened video""" 
        #sends the 'k' key, used for play and pause in youtube
        self._send_key('k', tabs='all')

    def pause(self):
        """pauses opened video"""
        #sends the 'k' key, used for play and pause in youtube
        self._send_key('k', tabs='all')

    def play_first(self): 
        """plays the first song in queue and remove from queue"""   
        #if no songs have been queued yet, do nothing
        if not len(self.queue) > 0:
            sys.stderr.write('SongQueue.play_first: no songs queued\n')
            return

        #any issues with self.driver, refer to the following
        # https://selenium-python.readthedocs.io/installation.html
        if self.driver == 'chrome':
            browser = webdriver.Chrome(executable_path="C://cs338//new//Musify-Me-Music-for-the-Moment-/chromedriver.exe")
        elif self.driver == 'firefox':
            #webbrowser.register("firefox", None, webbrowser.BackgroundBrowser("C:\Program Files\Mozilla Firefox\\firefox"))
            browser = webdriver.Firefox(executable_path='C:\WebDriver\\bin\geckodriver')
           
        #retreive earliest added url from song queue
        (first_url, song_len) = self.queue.pop(0) 
        #length could be useful in determining when to play next, maybe a timer as class attribute
        sys.stdout.write('playing a song for '+ str(song_len)+'s\n')
        #it would be cool to save the song title too, so we can give preview of next

        #play next song and add to open tabs
        browser.get(first_url)
        with self.tablock:
            self.tabs.append(browser)

        self.play()
        """
        t0 = time.time()
        keep_playing = True
        while(keep_playing):
            t1 = time.time()
            passed = t1 - t0
            print(passed)
            if(song_len - passed < 240):
                keep_playing = False
        self.pause()
        self.close_tab()
        """
        #webbrowser.get('firefox').open(url)

    def close_tab(self):
        if not len(self.tabs) > 0:
            sys.stderr.write('SongQueue.close_tab: no tabs open to close\n')
            return

        with self.tablock:    
            tab = self.tabs.pop(0)
            tab.close()

    def clear(self):
        """empties the song queue"""
        with self.qlock:
            self.queue = []

    def _send_key(self, key, tabs='one'):
        """sends a key to the browser opened by the queue.  Args: key(str)"""
        #sends the 'k' key, used for play and pause in youtube

        with self.tablock:
            for tab in self.tabs:
                elem = tab.find_element_by_xpath("/html")
                try: 
                    elem.send_keys(key) 
                    if tabs == 'one':
                        break 
                except Exception as e:
                    sys.stderr.write('send {} key failed\n'.format(key))
                    print(e)
                    sys.exit(-1)




"""
def test_SongQueue():
    KW1 = ['yunosuke', 'blank', 'catalyst']
    KW2 = ['reol', 'end']
    KW3 = ['tolerance', 'exotica']
    KEY = 'AIzaSyCjgFgk2bdUS8cr74K9wiopWDdfXhwgt9g'
    PAUSE = 5
    DRIVER = 'chrome'

    try: queue=SongQueue(KEY, driver=DRIVER)
    except Exception as e: 
        sys.stderr.write('could not create SongQueue\n')
        print(e)

    try: queue.add_by_kw(KW1)
    except Exception as e: 
        sys.stderr.write('could not query {}\n'.format(KW1))
        print(e)

    try:queue.play_first()
    except Exception as e: 
        sys.stderr.write('SongQueue.play_first failed\n')
        print(e)

    time.sleep(PAUSE)
    try: queue.clear()
    except exception as e:
        sys.stderr.write('SongQueue.clear failed\n')
        print(e)

    try:queue.add_by_kw(KW2)
    except Exception as e: 
        sys.stderr.write('could not query {}\n'.format(KW2))
        print(e)
    
    try:queue.pause()
    except Exception as e: 
        sys.stderr.write('SongQueue.pause failed\n')
        print(e)

    time.sleep(PAUSE)

    try:queue.play()
    except Exception as e: 
        sys.stderr.write('SongQueue.play failed\n')
        print(e)

    time.sleep(PAUSE)

    try: queue.close_tab()
    except Exception as e:
        sys.stderr.write('SongQueue.pause failed\n')
        print(e)

    try:queue.play_first()
    except Exception as e: 
        sys.stderr.write('SongQueue.play_first failed\n')
        print(e)

    try:queue.add_by_kw(KW3)
    except Exception as e: 
        sys.stderr.write('could not query {}\n'.format(KW3))
        print(e)

    try:
        sys.stdout.write('current queue: ')
        print(queue.show_queue())
    except Exception as e:
        sys.stderr.write('an error occured while printing queue')
        print(e)
    sys.stdout.write('SongQueue tests complete')

test_SongQueue()
"""