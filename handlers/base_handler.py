import json
import webapp2


class BaseHandler(webapp2.RequestHandler):
    HTTP_OK = 200
    HTTP_OK_CREATED = 201
    HTTP_BAD_REQUEST = 400
    HTTP_NOT_FOUND = 404
    HTTP_ERROR = 500

    def response_ok_raw(self, message):
        response = webapp2.Response(message)
        response.set_status(self.HTTP_OK)

        return response

    def response_ok(self, data={}):
        response = webapp2.Response(json.dumps(data))
        response.set_status(self.HTTP_OK)

        return response

    def response_error(self, message, traceback=None):
        error_data = {"message": str(message)}

        if traceback:
            error_data["traceback"] = traceback

        response = webapp2.Response(json.dumps({"error": error_data}))
        response.set_status(self.HTTP_ERROR)

        return response
