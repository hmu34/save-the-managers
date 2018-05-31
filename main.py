import json
import webapp2

from request_handler_factory import RequestHandlerFactory


class MainPage(webapp2.RequestHandler):
    def post(self):
        event = self._parse_event(self.request.body)
        handler = RequestHandlerFactory().get(event['type'])
        return handler.handle(event)

    def _parse_event(self, raw_data):
        data = json.loads(raw_data)
        return data


app = webapp2.WSGIApplication([
    ('/api', MainPage),
], debug=True)
