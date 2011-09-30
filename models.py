#!/usr/bin/env python
from google.appengine.ext import db

class SearchData(db.Model):
    queryText           = db.TextProperty()
    active              = db.BooleanProperty()
    created             = db.DateTimeProperty(verbose_name=None, auto_now=False, auto_now_add=True)
    lastQuery           = db.DateTimeProperty(verbose_name=None, auto_now=True)
#    videoReferenceList  = db.ListProperty(default=None,verbose_name=None)

class VideoData(db.Model):
    json                = db.TextProperty()
    views               = db.TextProperty()
    token               = db.TextProperty()
    alertLevel	    	= db.TextProperty()
    checkMeFlag         = db.BooleanProperty()
    associatedSearch    = db.ListProperty(str)
