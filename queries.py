class SelectVideosBySearchTerm():
    
    def __init__(self):
        pass
    
    def dictionary(self, search_term):
        
        from models import VideoData, VideoSearchIndex, SearchData, VideoViewsData
        import logging
        from main import DATE_STRING_FORMAT
        
        displayDictionary = {}
        
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
                
                    # Create a list of date-stamped views records for each video
                    viewsQuery = video.views.order('dateTime')
                                
                    # reset the iterator
                    i = 0

                    for record in viewsQuery:
                        
                        # have to declare these vars to make sure that they are floats
                        viewsSpeed = 0.
                        viewsAcceleration = 0.
                        
                        # can't calculate speed/acceleration if there is only one entry
                        if i > 0:
                            viewsSpeed, viewsAcceleration = CalculateViewData().viewData(record, previousRecord, previousSpeed)

                        # We need to store the record for next time around
                        previousRecord = record
                        previousSpeed = viewsSpeed
                    
                        # create a dictionary for each entry containing this data
                        dataDict = {"datetime": record.dateTime.strftime(DATE_STRING_FORMAT), "views": record.views, "speed": viewsSpeed, "acceleration": viewsAcceleration}

                        # append this new dictionary to the list.
                        dataList.append(dataDict)
                    
                        # iterate counter
                        i = i +1
                
                    # turn info into dictionary
                    videoInfo = eval(video.json)
                        
                    # iterate and create big dictionary
                    videoDictionary = { "info" : videoInfo, "data" : dataList}
                    videoList.append(videoDictionary)
                    videoIndex = videoIndex + 1
            
                displayDictionary[search.queryText] =  videoList
               
            return displayDictionary



############################################ Retrieve recent searches  ###################################################

class RecentSearches():
     def __init__(self):
         pass

     def generate(self):
         from models import SearchData, VideoSearchIndex

         # Construct a query to get all the searches
         searchesQuery = SearchData.all().order('-created')

         # Create an empty list to hold these 
         resultsList = []

         # Go through each search in the database
         for search in searchesQuery:

             # filter videos by search. this is quick because it just holds keys *?*
             videosBySearch = VideoSearchIndex.all().filter('searchTerms = ', search)
             videosCount = videosBySearch.count()
             search.count = videosCount
             search.urlSafeQueryText = str(search.queryText).replace(' ', '+')

             # chuck each one at the end of the list
             resultsList.append(search)

         return resultsList
         

############################################ Calculate view data  ###################################################

class CalculateViewData():
    
    def __init__(self):
        
        pass
    
    def viewData(self, recordA, recordB, recordBSpeed):
        
        # have to declare these vars to make sure that they are floats
        viewsSpeed = 0.
        viewsAcceleration = 0.
        
        # get a timedelta object for how much time has passed
        timeDelta = recordA.dateTime - recordB.dateTime
        timeDeltaSeconds = float((timeDelta.microseconds + (timeDelta.seconds + timeDelta.days * 24 * 3600) * 10**6) / 10**6)

        # get the change in the views
        viewsDelta = float(recordA.views - recordB.views)

        # calculate the average speed since the last check in vps
        recordASpeed = float(viewsDelta / timeDeltaSeconds) * 60 * 60

        # calculate the change in speed
        speedDelta = recordASpeed - recordBSpeed
        viewsAcceleration = speedDelta / timeDeltaSeconds * 60 * 60
        
        return viewsSpeed, viewsAcceleration
        