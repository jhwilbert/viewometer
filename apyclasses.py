class MonitorVideos(webapp.RequestHandler):
    def get(self):
        """ 
        Selects videos from database and tracks their views over time
        """

        # get current datetime
        now = datetime.datetime.now()
        nowstr = now.strftime(DATE_STRING_FORMAT) # youtube consistent date format
        
        query = VideoData.gql("WHERE checkMeFlag = True")
        logging.info('Checking %i videos', query.count())        
        for video in query:
           #print self.getEntryData(video.token)
            
           # get id
           video_k = db.Key.from_path("VideoData", video.token)
           video_o = db.get(video_k)
           
           # add new key pair to dictionary
           viewsEntries = eval(video_o.views)
           viewsEntries.append({'time': nowstr, 'views': self.getEntryData(video.token), 'currentSpeed': 0, 'acceleration': 0})   
           
           video_o.views = simplejson.dumps(viewsEntries)
           video_o.checkMeFlag = False
           video_o.put()
           #video_o.delete()

      
    def getEntryData(self,entry_id):
        """ 
        Connect to YT service and gets video viewcount 
        """
        view_count = "0"

        # Connect to Youtube Service
        yt_service = gdata.youtube.service.YouTubeService()
        try:
            entry = yt_service.GetYouTubeVideoEntry(video_id=entry_id)
            if entry.statistics:
                view_count = entry.statistics.view_count
                
        except gdata.service.RequestError:
            logging.error('request error')
        
        return view_count
        
class StoreVideos(webapp.RequestHandler):    
    def get(self):
        """ 
        Connects to DataStore model checks if any data has been stored under the same date, 
        If not gets the entries from Youtube API and stores them in that day.
        """

        # Connect to Youtube Service
        yt_service = gdata.youtube.service.YouTubeService()        
        feed = yt_service.GetMostRecentVideoFeed()       
        
        tokens = []
        dataModelRetrieve = VideoData()  
               
        # Creates Array with all elements
        for tokenid in dataModelRetrieve.all():
            tokens.append(tokenid.token)
            
        # Checks for videos and just adds the new ones
        for entry in feed.entry:
                        
            vidtoken = entry.media.player.url[31:-29] # stripping youtube + gdata path junk

            dataModelStore = VideoData(key_name=vidtoken)
            dataModelStore.token = vidtoken
            dataModelStore.json = simplejson.dumps(self.getVideoInfo(entry))
            dataModelStore.views = simplejson.dumps(self.getVideoViews(entry))
            dataModelStore.alertLevel = "initial"
            dataModelStore.checkMeFlag = False
            dataModelStore.put() 
            ##db.delete(dataModelStore.all()) #### DELETE ALL ENTRIES
              
        
    def getVideoInfo(self,entry):
        """ 
        Connects to Youtube API, gets the feed of most recent videos and parses each 
        entry into a dictionary.
        """
        thumbs = []

        # check if Youtube is returning all objects
        if  entry.media.title:
            title = entry.media.title.text
        else:
            title = "Couldn't retrieve title"
        if  entry.published:

            date_published = entry.published.text[0:-8] # to simplify we take out milliseconds of date published
        else:
            date_published = "Couldn't retrieve date"
        
        if entry.media.player:
            url = entry.media.player.url           
        else:
            url = "Couldn't retrieve URL"
        if entry.media.thumbnail:
            for thumbnail in entry.media.thumbnail:
                thumbs.append(thumbnail.url)
        else:
            thumbs = []
        
        # add them to a dict
        video = { "title" : title, "date_published" : date_published, "url" : url, "thumbs" : thumbs}
        
        return video

    def getVideoViews(self,entry):
        """ 
        Get video views and store them in a separate entity
        """
        
        viewsEntries = []
    
        # get current datetime
        nowstr = datetime.datetime.now().strftime(DATE_STRING_FORMAT) # youtube consistent date format
    
        if entry.statistics:
            viewcount = entry.statistics.view_count
            viewsEntries.append({'time': nowstr, 'views': viewcount, 'currentSpeed': 0, 'acceleration': 0})    
        else:
            viewsEntries.append({'time': nowstr, 'views': 0, 'currentSpeed': 0, 'acceleration': 0})                            
        
        return viewsEntries