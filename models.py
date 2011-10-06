#!/usr/bin/env python
from google.appengine.ext import db

class SearchData(db.Model):
    queryText           = db.StringProperty()
    active              = db.BooleanProperty(required=True, default=True)
    created             = db.DateTimeProperty(verbose_name=None, auto_now=False, auto_now_add=True)
    lastQuery           = db.DateTimeProperty(verbose_name=None, auto_now=True)

class VideoData(db.Model):
    json                = db.TextProperty()
    views               = db.TextProperty()
    token               = db.StringProperty()
    alertLevel	    	= db.StringProperty()
    checkMeFlag         = db.BooleanProperty()

class VideoSearchIndex(db.Model):
    searchTerms         = db.ListProperty(db.Key)