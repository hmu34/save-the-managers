import logging

from base_handler import BaseHandler


class EventCallbackHandler(BaseHandler):
    def handle(self, event):
        logging.warn(event)
        return self.response_ok_raw("Good!")
