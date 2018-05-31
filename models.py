from google.appengine.ext import ndb

class User(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    slack_token = ndb.StringProperty()
    session_id = ndb.StringProperty()

    @classmethod
    def query_by_id(cls, id):
        return User.get_by_id(id)

    @classmethod
    def query_by_session_id(cls, session_id):
        return User.query(session_id=session_id)[0]
