from base_handler import BaseHandler


class RateLimitedHandler(BaseHandler):
    def handle(self, data):
        return self.response_ok_raw("Bad!")
