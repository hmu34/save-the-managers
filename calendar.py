from google.appengine.api import urlfetch

import json
import datetime

class Calendar(object):

    """
        If not busy, returns false
        If busy returns the current event list
    """
    def is_busy(self, date, access_token):
        time = self.build_date_range(date)
        return self.get_events(time['timeMin'], time['timeMax'], access_token)

    def build_date_range(self, date):
        timeMax = date + datetime.timedelta(seconds=1)
        return {'timeMin': date.isoformat() + 'Z', 'timeMax': timeMax.isoformat() + 'Z'}

    # Time is in iso (2018-05-30T00:00:00.000Z) format
    def get_events(self, timeMin, timeMax, access_token):
        url="https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin={timeMin}&timeMax={timeMax}&singleEvents=true".format(timeMin=timeMin, timeMax=timeMax)
        result = urlfetch.fetch(
            url=url,
            method=urlfetch.GET,
            headers={"Authorization": "Bearer {}".format(access_token)})

        items = json.loads(result.content).get("items")
        if items is None:
            return items

        items = filter(lambda x: x['status'] == 'confirmed', items)
        items = filter(Calendar.is_not_available, items)
        items = filter(lambda x: Calendar.is_attending(x) or Calendar.is_organizer(x), items)
        return map(Calendar.map_event, items)

    @staticmethod
    def map_event(event):
        return {'summary': event.get('summary'),
            'private': bool(Calendar.is_private(event)),
            'start': event.get('start'),
            'end': event.get('end'),
            'location': event.get('location'),
            }

    @staticmethod
    def is_attending(event):
        return filter(lambda y: y.get('self') == True and y['responseStatus'] == 'accepted', event.get('attendees',[]))

    @staticmethod
    def is_organizer(event):
        return event.get('organizer').get('self')

    @staticmethod
    def is_not_available(event):
        return event.get('transparency') != 'transparent'

    @staticmethod
    def is_private(event):
        return event.get('visibility') == 'private'

