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
schedule = zermelo_api.get_schedule(access_token, cancelled=False, start=start, end=end, fields="subjects,teachers")

# create users
moodle_api.base_url("http://google.com/")
user_token = moodle_api.get_user_token('ws_user', '274!TzZ1XioI')['token']

teachers_completed = [] # List of all teachers that have been processed (prevent duplicates)
users = [] # List of all users to be created

# Loop through all appointments
for entry in schedule['response']['data']:
    # Loop through all teachers
    for teacher in entry['teachers']:
        # Verify duplicate
        if not teacher in teachers_completed:
            # Add to dictionary
            teachers_completed.append(teacher)
            users.append(zermelo_api.get_user(access_token, teacher))

moodle_api.create_users(user_token, users)