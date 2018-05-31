import webapp2

from google.appengine.api import urlfetch
from handlers.base_handler import BaseHandler
import config


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

        return self.response_ok_raw(result.content)


app = webapp2.WSGIApplication([
    ('/google-auth/callback', AuthCallback),
], debug=True)
