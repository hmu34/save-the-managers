from base_handler import BaseHandler


class UrlVerificationHandler(BaseHandler):
    def handle(self, data):
        return self.response_ok_raw(data['challenge'])
