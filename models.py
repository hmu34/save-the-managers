from google.appengine.ext import ndb


class User(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    slack_token = ndb.StringProperty()
    session_id = ndb.StringProperty()
    google_access_token = ndb.StringProperty()
    google_refresh_token = ndb.StringProperty()
    google_token_expiry_time = ndb.IntegerProperty()

    whitelist_names = ndb.StringProperty(repeated=True)
    blacklist_names = ndb.StringProperty(repeated=True)
    whitelist_ids = ndb.StringProperty(repeated=True)
    blacklist_ids = ndb.StringProperty(repeated=True)

    @classmethod
    def query_by_id(cls, id):
        return User.get_by_id(id)

    @classmethod
    def query_by_session_id(cls, session_id):
        return User.query(User.session_id == session_id).fetch(1)[0]
