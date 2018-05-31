import json
import webapp2
import uuid
from google.appengine.api import urlfetch

from handlers.base_handler import BaseHandler
import models

import config


class AuthRedirect(webapp2.RequestHandler):
    def get(self):
        return self.redirect('https://slack.com/oauth/authorize?client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}'.format(client_id=config.OAUTH_CLIENT_ID, scope=config.OAUTH_SCOPE, redirect_uri=config.OAUTH_CALLBACK_URI))


class AuthCallback(BaseHandler):
    def get(self):
        code = self.request.get("code", None)
        result = urlfetch.fetch(
            url='https://slack.com/api/oauth.access',
            payload='grant_type=authorization_code&redirect_uri={callback_uri}&code={code}&client_id={client_id}&client_secret={client_secret}'.format(
                callback_uri=config.OAUTH_CALLBACK_URI, code=code, client_id=config.OAUTH_CLIENT_ID, client_secret=config.OAUTH_CLIENT_SECRET),
            method=urlfetch.POST,
            headers={"Content-Type": "application/x-www-form-urlencoded"})

        data = json.loads(result.content)
        access_token = data['access_token']
        user_id = data['user_id']

        user = models.User.query_by_id(user_id)
        if user is None:
            user = models.User(id=user_id, slack_token=access_token, session_id=uuid.uuid4().hex)
        else:
            user.slack_token = access_token
            user.session_id = uuid.uuid4().hex

        user.put()
        return self.redirect(config.CONFIGURE_URI.format(session_id=user.session_id))


app = webapp2.WSGIApplication([
    ('/auth', AuthRedirect),
    ('/auth/callback', AuthCallback)
], debug=True)
