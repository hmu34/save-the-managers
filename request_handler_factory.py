from handlers.url_verification import UrlVerificationHandler
from handlers.event_callback import EventCallbackHandler
from handlers.rate_limited import RateLimitedHandler


class RequestHandlerFactory():
    def get(self, event_type):
        if event_type == "event_callback":
            return EventCallbackHandler()
        elif event_type == "url_verification":
            return UrlVerificationHandler()
        elif event_type == "app_rate_limited":
            return RateLimitedHandler()
        else:
            raise Exception("Unknown event type")
