from google.appengine.api import urlfetch

import json
import datetime
import config
import models

class Calendar(object):

    """
        If not busy, returns false
        If busy returns the current event list
    """
    def is_busy(self, date, user_id):
        access_token = self.get_token(user_id)
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

    def get_token(self, user_id):
        user = models.User.get_by_id(user_id)
        token_expiry_datetime = datetime.fromtimestamp(user['google_token_expiry_time'])
        current_datetime = datetime.datetime.now()
        if token_expiry_datetime <= current_datetime:
            # Refresh!
            return self.do_refresh_token(user)
        return user['google_access_token']

    def do_refresh_token(self, user):
        result = urlfetch.fetch(
            url='https://accounts.google.com/o/oauth2/token',
            payload='grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}'.format(
                refresh_token=user['google_refresh_token'], client_id=config.GOOGLE_CLIENT_ID, client_secret=config.GOOGLE_CLIENT_SECRET),
            method=urlfetch.POST,
            headers={"Content-Type": "application/x-www-form-urlencoded"})

        data = json.loads(result.content)

        user.google_access_token = data['access_token']
        user.google_token_expiry_time = int(time.time()) + data['expires_in']
        user.put()

        return user.google_access_token

    @staticmethod
    def map_event(event):
        return {'summary': event.get('summary'),
            'private': bool(Calendar.is_private(event)),
            'start': Calendar.calendar_date_to_ts(event.get('start')),
            'end': Calendar.calendar_date_to_ts(event.get('end')),
            'location': event.get('location'),
            }

    @staticmethod
    def calendar_date_to_ts(date):
        if "dateTime" in date:
            date_string = date['dateTime'].replace('+02:00','')
            delta = datetime.timedelta(hours=2)
            corrected_date = datetime.datetime.strptime(date_string,'%Y-%m-%dT%H:%M:%S') + delta
            return corrected_date.strftime("%s")
        elif "date" in date:
            date_string = date['date']
            delta = datetime.timedelta(hours=2)
            corrected_date = datetime.datetime.strptime(date_string,'%Y-%m-%d') + delta
            return corrected_date.strftime("%s")

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

