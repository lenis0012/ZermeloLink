# Imports
import urllib
import urllib2
import os.path
import json
import datetime
import uuid

# Static values
zermelo_api_base_url = "https://kwcollege.zportal.nl/api/v3"
zermelo_api_token = "/oauth/token"
zermelo_api_appointment = "/appointments"
zermelo_api_users = "/users"


# Request access token from zermelo
def get_access_token():
    if os.path.isfile("auth_token.json"):
        # Load auth token from file
        f = open("auth_token.json", 'r')
        data = json.loads(f.read())
    else:
        # Request an auth token from apis
        api_code = raw_input("Please insert a Zermelo linking code: ").replace(" ", "")
        api_url = zermelo_api_base_url + zermelo_api_token
        post_data = {
            'grant_type': 'authorization_code',
            'code': api_code
        }
        encoded_post_data = urllib.urlencode(post_data)
        response = urllib2.urlopen(api_url, encoded_post_data)
        data = json.loads(response.read())
        f = open("auth_token.json", 'w')
        json.dump(data, f)
    return _AccessToken(data)


# Get schedule from zermelo
def get_schedule(access_token, start=None, end=None, user='~me', fields=None, valid=True, cancelled=True, base=False):
    params = {
        'valid': valid,
        'cancelled': cancelled,
        'base': base,
        'access_token': access_token.get_token()
    }

    if start is not None:
        params['start'] = start # Start date
    if end is not None:
        params['end'] = end # End date
    if user is not None:
        params['user'] = user # user code
    if fields is not None:
        params['fields'] = fields # fields filter

    url = zermelo_api_base_url + zermelo_api_appointment + "?" + urllib.urlencode(params)
    request = urllib2.urlopen(url)
    return json.load(request)


# Get user data by code
def get_user(access_token, code):
    # Set parameters
    params = {
        'code': code,
        'access_token': access_token.get_token()
    }

    # Request user data from zermelo
    url = zermelo_api_base_url + zermelo_api_users + "?" + urllib.urlencode(params)
    request = urllib2.urlopen(url)
    response = json.load(request)['response']
    data = response['data']

    # test purposes
    data = {
        'email': str(uuid.uuid4().get_hex().upper()[0:6]) + '@abcd.nl',
        'firstName': code,
        'lastName': 'Last',
        'prefix': ''
    }

    # Parse data
    data['code'] = code
    email = data['email']
    fname = data['firstName']
    lname = data['lastName']
    mname = data['prefix']
    userobject = {
        'username': code,
        # 'createpassword': 1,
        'firstname': fname,
        'lastname': lname,
        'email': email,
        'middlename': mname
    }
    return data


# Parse json schedule
def parse_schedule(schedule):
    return _Schedule(schedule)


# Schedule data class
class _Schedule(dict):

    def __init__(self, data):
        super(_Schedule, self).__init__()
        # Create empty dictionary of appointments
        for i in range(5):
            self[i] = list()
        # Check if response was valid
        self._valid = data['response']['status'] is 200
        for entry in data['response']['data']:
            if entry['start'] is None or entry['startTimeSlot'] is None:
                continue
            # Get start time of the appointment
            start = datetime.datetime.fromtimestamp(entry['start'])
            # Add to dictionary
            self[start.weekday()].append(_Appointment(entry))
        for arr in self.itervalues():
            arr.sort(key=lambda app: app.get_start_slot())

    def get_serializable_version(self):
        map = dict()
        for k,v in self.iteritems():
            apps = list()
            for a in v:
                apps.append(a._get_raw_data())
            map[k] = apps
        return map

# Appointment data class
class _Appointment:

    def __init__(self, data):
        self._data = data
        self._locations = data['locations']
        self._groups = data['groups']
        self._teachers = data['teachers']
        self._start_time_slot = data['startTimeSlot']
        self._end_time_slot = data['endTimeSlot']
        self._start = data['start']
        self._end = data['end']
        self._moved = data['moved']
        self._valid = data['valid']
        self._hidden = data['hidden']
        self._cancelled = data['cancelled']
        self._change_description = data['changeDescription']

    def _get_raw_data(self):
        return self._data

    def get_locations(self):
        return self._locations

    def get_groups(self):
        return self._groups

    def get_teachers(self):
        return self._teachers

    def get_start_slot(self):
        return self._start_time_slot

    def get_end_slot(self):
        return self._end_time_slot

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end


# Container for access token
class _AccessToken:

    def __init__(self, data):
        self.data = data

    def get_token(self):
        return self.data['access_token']

    def get_expiry(self):
        return self.data['expires_in']

    def get_type(self):
        return self.data['token_type']
