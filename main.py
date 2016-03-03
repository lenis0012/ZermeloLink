import time

from datetime import datetime, timedelta
from app.apis import zermelo_api, moodle_api

now = datetime.now()
start = now - timedelta(days=now.weekday(), hours=now.hour-1)
end = start + timedelta(days=5)
if now.weekday() is 5 or now.weekday() is 6:
    start = start + timedelta(weeks=1)
    end = end + timedelta(weeks=1)
start = int(time.mktime(start.timetuple()))
end = int(time.mktime(end.timetuple()))

# aquire schedule from zermelo
access_token = zermelo_api.get_access_token()
schedule = zermelo_api.get_schedule(access_token, user=None, cancelled=False, start=start, end=end, fields="subjects,teachers")

# create users
user_token = moodle_api.base_url("http://kwcollege.zermelo.nl/")
moodle_api.create_users(user_token, schedule['users'])