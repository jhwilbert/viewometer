#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Google
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext.webapp import template

# Youtube
import gdata.youtube.service

# Other
from BeautifulSoup import BeautifulSoup
import gaemechanize
import simplejson
import sys
import html2text
import simplejson
import logging
import datetime
import os
import time
from urllib2 import HTTPError

# Models

# Constants
HOST = "http://localhost:8082/"
DATE_STRING_FORMAT = "%Y-%m-%dT%H:%M"
TEN_MINUTES = datetime.timedelta(minutes=1)
THIRTY_MINUTES = datetime.timedelta(minutes=30)
ONE_HOUR = datetime.timedelta(hours=1)
HALF_DAY = datetime.timedelta(hours=12)
ONE_DAY = datetime.timedelta(days=1)
ALERT_LEVELS = {'initial': TEN_MINUTES,
               'regular': HALF_DAY,
               'low': ONE_DAY,
               'high': THIRTY_MINUTES}

############################################ Main #########################################################

class MainHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

############################################ Main #########################################################

class SearchHandler(webapp.RequestHandler):
    def get(self):
        
        
        path = os.path.join(os.path.dirname(__file__), 'search.html')
        self.response.out.write(template.render(path, {}))


############################################ Display Mechanism ############################################   

class DisplayVideos(webapp.RequestHandler):  
    
    from decimal import *
       
    def get(self):
        
        
        from models import VideoData, VideoSearchIndex, SearchData, VideoViewsData
        
        """ 
        Displays all videos.        
        """
        
        # get the search term from the web request
        search_term = self.request.get("search")
        
        displayDictionary = {}
        
        
        if search_term:
            
            # so that I can find this in the log TODO: remove
            logging.info('***************************************')
            
            # query to find all the saved searches that match the string
            searchesQuery = SearchData.all().filter('queryText = ', search_term) # order by priority TODO
            logging.info('number of searches for %s: %i (should only ever be one)', search_term, searchesQuery.count())
            
            # if there is any result at all
            if searchesQuery.get():
                
                # for each search that matches
                for search in searchesQuery:
            
                    # query to find all the videos that were found using this search term
                    videosBySearch = VideoSearchIndex.all().filter('searchTerms = ', search)
                    logging.info('number of videos for this search: %i', videosBySearch.count())
                    
                    videoList = []
                    videoIndex = 0
                    videoInfo = {}
                    dataList = []
                    
                    # each video in the result set
                    for videoSearchIndex in videosBySearch:
                        dataList = []
                        
                        video = videoSearchIndex.parent()
                        
                        logging.info("title %s", video.json)

                        # Create a list of date-stamped views records for each video
                        viewsQuery = video.views.order('dateTime')
                        
                        logging.info('viewsQuery %i', viewsQuery.count())
                        
                        # reset the iterator
                        i = 0

                        for record in viewsQuery:
                            
                            # have to declare these vars to make sure that they are floats
                            viewsSpeed = 0.
                            viewsAcceleration = 0.

                            # can't calculate speed/acceleration if there is only one entry
                            if i > 0:

                                # get a timedelta object for how much time has passed
                                timeDelta = record.dateTime - previousRecord.dateTime
                                timeDeltaSeconds = float((timeDelta.microseconds + (timeDelta.seconds + timeDelta.days * 24 * 3600) * 10**6) / 10**6)
                                logging.info("timeDeltaSeconds %i", timeDeltaSeconds)

                                # get the change in the views
                                viewsDelta = float(record.views - previousRecord.views)
                                logging.info("viewsDelta %i", viewsDelta)

                                # calculate the average speed since the last check in vps
                                viewsSpeed = float(viewsDelta / timeDeltaSeconds) * 60 * 60
                                logging.info("viewsSpeed %f", viewsSpeed)

                                # calculate the change in speed
                                speedDelta = viewsSpeed - previousSpeed
                                viewsAcceleration = speedDelta / timeDeltaSeconds * 60 * 60
                                logging.info("viewsAcceleration %f", viewsAcceleration)


                            # We need to store the record for next time around
                            previousRecord = record
                            previousSpeed = viewsSpeed
                            
                            # create a dictionary for each entry containing this data
                            dataDict = {"datetime": record.dateTime.strftime(DATE_STRING_FORMAT), "views": record.views, "speed": viewsSpeed, "acceleration": viewsAcceleration}
                            logging.info("dataDict %s", dataDict)

                            # append this new dictionary to the list.
                            dataList.append(dataDict)
                            
                            # iterate counter
                            i = i +1
                        
                        # turn info into dictionary
                        videoInfo = eval(video.json)
                    
                        logging.info('videoIndex %i', videoIndex)
                    
                        # iterate and create big dictionary
                        videoDictionary = { "info" : videoInfo, "data" : dataList}
                        videoList.append(videoDictionary)
                        videoIndex = videoIndex + 1
                    
                    displayDictionary[search.queryText] =  videoList
                       
            # parse dictionary into json
            #result = simplejson.dumps(displayDictionary)

            #self.response.headers['Content-Type'] = 'application/json'
            #self.response.out.write(result)
            return displayDictionary
            
        else:
            print "No search term attached"
                        
            
############################################ Storing Mechanism ############################################     
        
class SelectBatch(webapp.RequestHandler):
    def get(self):
        from models import VideoData, VideoViewsData
        
        """
        Selects the videos from the database that are due a check. This is based on the amount of time since they were last checked and on their alert level.
        """
        
        # find the time now
        now = datetime.datetime.now()

        queryModel = VideoData.all()
        count = 0
        
        for video in queryModel:
            
            # get all the views info for that video
            video_views_data = video.views.order("-dateTime")
            
            # get the last one
            latest_views_data = video_views_data.get()
            
            #compare the times
            timeElapsed = now - latest_views_data.dateTime
            
            # if the amount of time passed since last check exceeds the alertLevel for this video
            if (timeElapsed > ALERT_LEVELS[video.alertLevel]): 
                video.checkMeFlag = True
                count += 1
            else:
                video.checkMeFlag = False
            
            video.put()
        
        logging.info('Selected %i videos for checking', count)    

#class SearchRoutine(webapp.RequestHandler):
#    def get(self):
#        from models import SearchData
        
            
class ScrapePage(webapp.RequestHandler):
     def get(self):
          from models import VideoData, VideoSearchIndex, SearchData, VideoViewsData
          """
          Resource retrieves 20 most recent videos of You Tube given a search term. It retrieves them and stores in a datastore object
          using Mechanize and Beautiful soup.
          
          Resource usage:
          
          /tasks/scrape_page?search=term
          
          """
          search_term = self.request.get("search")
          
          logging.info("Executing")
          
          existing_search_query = db.GqlQuery("SELECT __key__ FROM SearchData WHERE queryText = :1", search_term)
          existing_search = existing_search_query.get()
          if existing_search is None:
              logging.info("No existing search_term matches: %s", search_term)
              new_search = SearchData()
              new_search.queryText = search_term
              new_search.put()
              search_query_key = new_search.key()
          else:
              logging.info("Found existing search_term: %s", existing_search)
              search_query_key = existing_search
          
          
          br = gaemechanize.Browser()
          
          # Browser options
          br.set_handle_equiv(True)
          br.set_handle_gzip(True)
          br.set_handle_redirect(True)
          br.set_handle_referer(True)
          br.set_handle_robots(False)

          # User-Agent (this is cheating, ok?)
          br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

          # The site we will navigate into, handling it's session
          br.open('http://www.youtube.com')
 
          # Scrape First Page Looking for Forms 
          br.select_form(nr=1)
          
          # Executes Query with Given Word
          br.form['search_query'] = search_term
          br.submit()
           
          # Finds all links the page
          search_links = [l for l in br.links()]
          
          linkcounter = 0

          for link in search_links:
              linkcounter  += linkcounter

          # Selects By Upload Rate (it's a hack now, needs to be context independent)         
          br.follow_link(search_links[16])
          
          html = br.response().read()          
          soup = BeautifulSoup(html)
          soup.prettify()
          
          #print soup
          
          # Creates Video List For Results
          search_results = soup.findAll('div', attrs = {'class': "result-item *sr "})
          
          # Store in DB
          new_video = VideoData()   
                   
          for result in search_results:
              
              # strip token from youtube url
              vidtoken =  self.scrapeVideoInfo(result)['url'][31:42] 
              
              # Create a new VideoData object with the video token
              new_video = VideoData(key_name=vidtoken)
              
              # If it doesn't exist already. TODO
              #if VideoData.get(new_video.key()) is None:
              new_video.token = vidtoken
              new_video.json = simplejson.dumps(self.scrapeVideoInfo(result))
              
              viewsDate, views = self.scrapeVideoViews(result)
              views_object = VideoViewsData(dateTime=viewsDate, views=views, video=new_video)
              views_object.put()
              
              new_video_searchlist = VideoSearchIndex(key_name=new_video.token, parent=new_video)    
              new_video_searchlist.searchTerms.append(search_query_key)
              new_video_searchlist.put()
                            
              new_video.alertLevel = "initial"
              new_video.checkMeFlag = False
              new_video.put()
          
                    
          #path = os.path.join(os.path.dirname(__file__), '/')
          self.response.out.write(HOST+"search?term="+search_term)

     def scrapeVideoInfo(self,result):
         """ All videos entries are within a href tag, so we have to go through each link 
         and find which one is which, so first URL is the link, third is title and so on....
         """
          
         # URL & Title - get first entry url
         urls = result.findAll('a')
         url = urls[0]['href']
         title = urls[3]['title']
         
         # Thumbnail - youtube has two image tags, testing which one is the real thumb
         
         #thumbs = result.findAll('img', attrs = {'alt' : 'Thumbnail'})

         thumb = result.findAll('img')[0];
         
         if thumb.has_key('data-thumb'):
             thumb_url = "http:" + thumb['data-thumb']
         else:
             thumb_url = "http:" + thumb['src']
         
         #print thumb_url
         
         # for thumb in thumbs:
         #              thumb_url = "http:" + thumb['src']           
         #              if thumb.has_key('data-thumb'):
         #                  thumb_url = "http:" + thumb['data-thumb']
         #          
         # Date Published - must do a calculator to get time object
         
         date_published = result.find('span', attrs = {'class' : 'date-added'}).find(text=True)
        
         date_published_str = self.formatDate(date_published).strftime(DATE_STRING_FORMAT)
         
         
         ############# TODO ################
         video = { "title" : title, "date_published" : date_published_str, "url" : "http://www.youtube.com" + url, "thumbs" : thumb_url }
         
         return video
     
     def formatDate(self,date):
        """ 
        Time calculator function that turns Youtube format x minutes ago into date 
        objects to store in DB
        """
                  
        # get current datetime
        now = datetime.datetime.now()
        dateList = date.split(" ")
        #upload_time = 0;
        
        #update current time with when the video was uploaded        
        if dateList[1] == "minutes" or dateList[1] == "minute":
            upload_time = now + datetime.timedelta(minutes=-(int(dateList[0]))) 
        if dateList[1] == "hour" or dateList[1] == "hours":
            upload_time = now + datetime.timedelta(hours=-(int(dateList[0])))

        return upload_time
        
     def scrapeVideoViews(self,result):

        viewsdict = {}

        # get current datetime
        now = datetime.datetime.now()
        #nowstr = now.strftime(DATE_STRING_FORMAT)
         
        viewcount = result.find('span', attrs = {'class' : 'viewcount'}).find(text=True)
        
        views = int(viewcount[0:-6])

        return now, views

class ScrapeViews(webapp.RequestHandler):
    def get(self):
        from models import VideoData, VideoViewsData
        """ 
        Selects videos from database and tracks their views over time
        """
        
        # get current datetime
        now = datetime.datetime.now()
        
        # query db for videos which have been flagged                   
        videos_to_check = VideoData.gql("WHERE checkMeFlag = True") # CHANGE THIS BACK TO TRUE WHEN DEPLOYING
        
        logging.info('Checking %i videos', videos_to_check.count()) 
               
        for video in videos_to_check:
                        
            # get the current number of views
            newViewsEntry = self.getEntryData(video.token)
            
            new_views_data = VideoViewsData(video=video, dateTime=now, views=newViewsEntry, collection_name="views")
            new_views_data.put()
            
            video.checkMeFlag = False
            video.put()
           
    def getEntryData(self,entry_id):
         """ 
         Connect to YT service and gets video viewcount 
         """
         
         view_count = 0
         br = gaemechanize.Browser()
         
         # Browser options
         br.set_handle_equiv(True)
         br.set_handle_gzip(True)
         br.set_handle_redirect(True)
         br.set_handle_referer(True)
         br.set_handle_robots(False)
         
         br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
         
         try:
            br.open('http://www.youtube.com/watch?v='+entry_id)
         
         except HTTPError, e:
             #print "Got error code", e.code
             pass
             
         html = br.response().read()          
         soup = BeautifulSoup(html)
         soup.prettify()
         
         for tabs in soup.findAll('span', {'class': 'watch-view-count'}):             
           view_count = str(tabs.contents[1]).lstrip('<strong>')[0:-9].replace(",", "") # this is a hack
         
         if(view_count):
             views = int(view_count)
         else:
             views = 0
         return views           

                                  
############################################ Handlers  ###################################################

def main():
    application = webapp.WSGIApplication([('/tasks/select_batch', SelectBatch),
                                          ('/tasks/scrape_page', ScrapePage),
                                          #('/tasks/search_routine', SearchRoutine),
                                          ('/tasks/scrape_views', ScrapeViews),
                                          ('/', MainHandler),
                                          ('/search', SearchHandler),
                                          ('/output/display_videos', DisplayVideos)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
