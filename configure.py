import os
import webapp2

from google.appengine.ext.webapp import template
from handlers.base_handler import BaseHandler
import models
import config
from slack_api import SlackApi


class ConfigurePage(BaseHandler):
    def get(self):
        success = self.request.get('success', None) == '1'
        session_id = self.request.get("session_id", None)
        path = os.path.join(os.path.dirname(__file__), 'templates', 'configure.html')
        google_oauth_redirect_uri = config.get_google_oauth_redirect_uri(session_id)

        user = models.User.query_by_session_id(session_id)

        is_authorized_with_google = user.google_access_token is not None
        user_profile = SlackApi().get_user_profile(user.slack_token, user.key.id())

        whitelist_1 = user.whitelist_names[0] if len(user.whitelist_names) > 0 else ""
        whitelist_2 = user.whitelist_names[1] if len(user.whitelist_names) > 1 else ""
        whitelist_3 = user.whitelist_names[2] if len(user.whitelist_names) > 2 else ""

        blacklist_1 = user.blacklist_names[0] if len(user.whitelist_names) > 0 else ""
        blacklist_2 = user.blacklist_names[1] if len(user.blacklist_names) > 1 else ""
        blacklist_3 = user.blacklist_names[2] if len(user.blacklist_names) > 2 else ""

        return self.response_ok_raw(template.render(path, {
            'success': success,
            'user_image': user_profile['image_72'],
            'user_name': user_profile['real_name'],
            'session_id': session_id,
            'google_oauth_redirect_uri': google_oauth_redirect_uri,
            'is_authorized_with_google': is_authorized_with_google,
            'whitelist_1': whitelist_1,
            'whitelist_2': whitelist_2,
            'whitelist_3': whitelist_3,
            'blacklist_1': blacklist_1,
            'blacklist_2': blacklist_2,
            'blacklist_3': blacklist_3,
        }))


class SavePage(BaseHandler):
    def get(self):
        whitelisted = filter(lambda x: x != "", [self.request.get('whitelist_1'), self.request.get('whitelist_2'), self.request.get('whitelist_3')])
        blacklisted = filter(lambda x: x != "", [self.request.get('blacklist_1'), self.request.get('blacklist_2'), self.request.get('blacklist_3')])
        session_id = self.request.get("session_id", None)

        user = models.User.query_by_session_id(session_id)
        user.whitelist_names = whitelisted
        user.blacklist_names = blacklisted
        user.whitelist_ids = map(lambda x: self._get_user_id(x), whitelisted)
        user.blacklist_ids = map(lambda x: self._get_user_id(x), blacklisted)
        user.put()

        self.redirect(config.CONFIGURE_URI_SUCCESS.format(session_id=session_id))

    def _get_user_id(self, name):
        user = SlackApi().get_user_by_name(config.BOT_ACCESS_TOKEN, name)
        if user is not None:
            return user['id']
        else:
            return None


app = webapp2.WSGIApplication([
    ('/configure/save', SavePage),
    ('/configure', ConfigurePage),
], debug=True)
