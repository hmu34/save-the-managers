import datetime
import logging
import random
import time

from base_handler import BaseHandler
from google_calendar import Calendar
from slack_api import SlackApi
import config
import models


class EventCallbackHandler(BaseHandler):
    GREETINGS = ["soy sebas", "sebas here"]
    FRIENDLY_MESSAGES = [
        u"Holaaaaa :) lo siento, ahora mismo estoy ocupadisimo, pero en cuanto salga de la meeting sobre {meeting}, te escribo y si quieres nos tomamos unas cerves en la chula, que invito yo. Te escribo en {minutes} minutos",
        u"ey, me pillas ahora mismo en una meeting de {meeting} que termina en {minutes} minutos. Llevo pensando en hablar contigo todo el dia, no te preocupes que enseguida te escribo y ... ;)"
    ]
    HATE_MESSAGES = [
        u"Pero vamos a ver, no te tengo dicho que me dejes en paz desgraciao. Estoy en una puta meeting de {meeting} mucho mas importante que hablar contigo. Cuando termine dentro de {minutes} minutos y vea si prefiero morirme o hablar contigo, ya si eso te hablo. Venga, que te pille un coche",
        u"No eres mas tonto porque no naciste antes. No has visto mi calendario? Estas ciego? Estoy en la reunion de {meeting} y aunque durara menos de {minutes} minutos que se lo que le queda, ya me buscare algo que hacer para no responderte. Al carrer ya hombre"
    ]

    NORMAL_MESSAGES = [
        u"Hola, perdona pero estoy ocupado ahora mismo en una reunion sobre {meeting}. Dentro de {minutes} minutos te escribo. Hasta ahora"
    ]

    def handle(self, event):
        payload = event['event']
        if payload['type'] == 'message':
            if self._is_autoreply(payload.get('text')):
                pass
            elif payload.get('text') in self.GREETINGS and\
                    config.BOT_USER in event['authed_users'] and\
                    payload.get('channel_type') == 'im':

                message = "Hi, please go here to configure your account: {url}".format(url=config.AUTH_URI)
                SlackApi().send_message(config.BOT_ACCESS_TOKEN, payload.get('channel'), message, False)

            elif payload.get('channel_type') == 'im':
                channel_id = payload.get('channel')
                users = filter(lambda x: x != payload.get('user'), event['authed_users'])
                if len(users) > 0:
                    dest_user = users[0]
                    user = models.User.query_by_id(dest_user)
                    if user is not None:
                        self._reply(channel_id, payload.get('user'), user)
                    else:
                        logging.warn('No user found for: ' + dest_user)
                else:
                    logging.warn('No users found for: ' + str(event))

        return self.response_ok_raw("Good!")

    def _is_autoreply(self, message):
        return any(map(lambda x: x.startswith(message[0:10]), self.FRIENDLY_MESSAGES + self.NORMAL_MESSAGES + self.HATE_MESSAGES))

    def _reply(self, channel_id, source_user_id, dest_user):
        events = Calendar().is_busy(datetime.datetime.now(), dest_user.key.id())
        if len(events) > 0:
            if source_user_id in dest_user.whitelist_ids:
                message = random.choice(self.FRIENDLY_MESSAGES)
            elif source_user_id in dest_user.blacklist_ids:
                message = random.choice(self.HATE_MESSAGES)
            else:
                message = random.choice(self.NORMAL_MESSAGES)

            message = message.format(
                meeting=events[0]['summary'],
                minutes=str(((int(events[0]['end']) - int(time.time())) / 60) - 240))

            SlackApi().send_message(dest_user.slack_token, channel_id, message, True)
