import json
from google.appengine.api import urlfetch


class SlackApi:
    BASE_PATH = "https://slack.com/api/{path}"

    def get_user_profile(self, token, user_id):
        return self._do_request(
            "users.profile.get",
            token,
            "user={user}".format(user=user_id)
        ).get('profile')

    def _do_request(self, path, token, payload=None):
        result = urlfetch.fetch(
            url=self.BASE_PATH.format(path=path),
            payload=payload,
            method=urlfetch.POST,
            headers={"Authorization": "Bearer " + token}
        )
        return json.loads(result.content)
