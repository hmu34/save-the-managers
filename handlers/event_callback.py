from base_handler import BaseHandler
from slack_api import SlackApi
import config


class EventCallbackHandler(BaseHandler):
    GREETINGS = ["soy sebas", "sebas here"]

    def handle(self, event):
        payload = event['event']
        if payload['type'] == 'message':
            if payload.get('text') in self.GREETINGS and\
                    config.BOT_USER in event['authed_users'] and\
                    payload.get('channel_type') == 'im':

                channel_info = SlackApi().get_channel_info(
                    config.BOT_ACCESS_TOKEN,
                    payload.get('channel'))

                message = "Hi, please go here to configure your account: {url}".format(url=config.AUTH_URI)
                SlackApi().send_message(config.BOT_ACCESS_TOKEN, channel_info['id'], message, False)

        return self.response_ok_raw("Good!")
