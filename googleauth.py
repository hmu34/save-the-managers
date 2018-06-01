import json
import time
import webapp2

from google.appengine.api import urlfetch
from handlers.base_handler import BaseHandler
import config
import models


class AuthCallback(BaseHandler):
    def get(self):
        session_id = self.request.get("state", None)
        code = self.request.get("code", None)

        result = urlfetch.fetch(
            url='https://accounts.google.com/o/oauth2/token',
            payload='grant_type=authorization_code&redirect_uri={redirect_uri}&code={code}&client_id={client_id}&client_secret={client_secret}'.format(
                redirect_uri=config.GOOGLE_REDIRECT_URI, code=code, client_id=config.GOOGLE_CLIENT_ID, client_secret=config.GOOGLE_CLIENT_SECRET),
            method=urlfetch.POST,
            headers={"Content-Type": "application/x-www-form-urlencoded"})

        data = json.loads(result.content)

        user = models.User.query_by_session_id(session_id)
        user.google_access_token = data['access_token']
        user.google_refresh_token = data['refresh_token']
        user.google_token_expiry_time = int(time.time()) + data['expires_in']
        user.put()

        return self.redirect(config.CONFIGURE_URI.format(session_id=session_id))


app = webapp2.WSGIApplication([
    ('/google-auth/callback', AuthCallback),
], debug=True)
