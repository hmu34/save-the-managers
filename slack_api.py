import json
import logging
from google.appengine.api import urlfetch


class SlackApi:
    BASE_PATH = "https://slack.com/api/{path}"

    def get_user_profile(self, token, user_id):
        return self._do_request(
            "users.profile.get",
            token,
            "user={user}".format(user=user_id)
        ).get('profile', {})

    def get_channel_info(self, token, channel):
        return self._do_request(
            "conversations.info",
            token,
            "channel={channel}".format(channel=channel)
        ).get('channel', {})

    def get_im_list(self, token):
        return self._do_request(
            "im.list",
            token).get('ims', [])

    def send_message(self, token, channel, message, as_user):
        return self._do_request(
            "chat.postMessage",
            token,
            "channel={channel}&text={message}&as_user={as_user}".format(
                channel=channel,
                message=message,
                as_user=("true" if as_user else "false"))
        )

    def _do_request(self, path, token, payload=None):
        result = urlfetch.fetch(
            url=self.BASE_PATH.format(path=path),
            payload=payload,
            method=urlfetch.POST,
            headers={"Authorization": "Bearer " + token}
        )

        return json.loads(result.content)
