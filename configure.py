import os
import webapp2

from google.appengine.ext.webapp import template
from handlers.base_handler import BaseHandler
import config


class ConfigurePage(BaseHandler):
    def get(self):
        session_id = self.request.get("session_id", None)
        path = os.path.join(os.path.dirname(__file__), 'templates', 'configure.html')
        google_oauth_redirect_uri = config.get_google_oauth_redirect_uri(session_id)
        return self.response_ok_raw(template.render(path, {'session_id': session_id, 'google_oauth_redirect_uri': google_oauth_redirect_uri}))


app = webapp2.WSGIApplication([
    ('/configure', ConfigurePage),
], debug=True)
