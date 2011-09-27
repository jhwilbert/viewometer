#!/usr/bin/env python
from google.appengine.ext import db

class VideoData(db.Model):
  json           = db.TextProperty()
  token           = db.TextProperty()