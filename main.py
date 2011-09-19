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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from BeautifulSoup import BeautifulSoup
from google.appengine.api import urlfetch

import gaemechanize
import simplejson
import sys
import html2text
import simplejson

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


class ScrapePage(webapp.RequestHandler):
     def get(self):

          br = gaemechanize.Browser()
          
          # Browser options
          br.set_handle_equiv(True)
          br.set_handle_gzip(True)
          br.set_handle_redirect(True)
          br.set_handle_referer(True)
          br.set_handle_robots(False)


          # Follows refresh 0 but not hangs on refresh > 0
          #br.set_handle_refresh(gaemechanize._http.HTTPRefreshProcessor(), max_time=1)

          # User-Agent (this is cheating, ok?)
          br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

          # The site we will navigate into, handling it's session
          br.open('http://www.youtube.com')
          print ''
          # Select the first (index zero) form
          #for f in br.forms():
          #    print ''
          #    print f
 
          # Scrape First Page Looking for Forms 
          br.select_form(nr=1)
          #print ''
          
          # Executes Query with Given Word
          br.form['search_query'] = 'cats'
          br.submit()
           
          # Finds all links the page
          search_links = [l for l in br.links()]
          
          linkcounter = 0   
          for link in search_links:
              linkcounter  = linkcounter + 1
              #print counter,link
          
          # Selects By Upload Rate (it's a hack now needs to be context independent)         
          br.follow_link(search_links[15])
          html = br.response().read()
          soup = BeautifulSoup(html)
          soup.prettify()
          
          # Creates Video Dictionary For Results
          search_results = soup.findAll('div', attrs={'class': 'result-item *sr '})
          
          videoData = {} 
          counter_vids = 0
          
          
          for result in search_results:
              
              counter_vids = counter_vids + 1
              
              # Gets Elements Within Result
              
              links = result.findAll('a')
              images = result.findAll('img', attrs = {'alt' : 'Thumbnail'})
              added = result.find('span', attrs = {'class' : 'date-added'}).find(text=True)
              viewcount = result.find('span', attrs = {'class' : 'viewcount'}).find(text=True)              

              for image in images:
                  thumb = "http:"+image['src']
              
              # builds final dict
              videoData[counter_vids] = { "thumb" : thumb, "dateadded" : added, "viewcount" : viewcount, "link" : "http://www.youtube.com/" + str(links[0]['href'])} # stores in dict
              
          finalResult = simplejson.dumps(videoData)    
          print finalResult

def main():
    application = webapp.WSGIApplication([('/', ScrapePage)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
