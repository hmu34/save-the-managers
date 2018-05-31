from google.appengine.ext import ndb

class User(ndb.Model):
    """Models an individual user """
    #id = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
