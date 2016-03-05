import time

from web import main as web
from datetime import datetime, timedelta
from app.apis import zermelo_api, moodle_api

# Lambda methods
users_to_names = lambda x: x['username']

# Get time frame (1 week)
now = datetime.now()
start = now - timedelta(days=now.weekday(), hours=now.hour-1)
end = start + timedelta(days=5)
if now.weekday() is 7 or now.weekday() is 6:
    start = start + timedelta(weeks=1)
    end = end + timedelta(weeks=1)
start = int(time.mktime(start.timetuple()))
end = int(time.mktime(end.timetuple()))

# aquire schedule from zermelo
zermelo_token = zermelo_api.get_access_token()
schedule = zermelo_api.get_schedule(zermelo_token, cancelled=False, start=start, end=end, fields="subjects,teachers")

# Define moodle token
moodle_api.base_url("http://localhost/moodle/")
moodle_token = moodle_api.get_user_token('ws_user', '274!TzZ1XioI')['token']
print moodle_token

users = []  # List of all users on schedule
subjects = {}  # Dictionary of all subjects and which teachers are attached to it

# Get list of all teachers and subjects
for entry in schedule['response']['data']:
    for teacher in entry['teachers']:
        if teacher not in users:
            users.append(teacher)
            # Subject
            for e in entry['subjects']:
                if e not in subjects:
                    subjects[e] = []
                subjects[e].append(teacher)

# Create users if needed
#existing_users = map(users_to_names, moodle_api.get_users(moodle_token, users))
existing_users = []
user_ids = {}
for user in moodle_api.get_users(moodle_token, users):
    existing_users.append(user['username'])
    user_ids[user['username']] = user['id']

create_users = []
for user_code in users:
    if user_code not in existing_users:
        user = zermelo_api.get_user(zermelo_token, user_code)
        create_users.append(user)

for user in moodle_api.create_users(moodle_token, create_users):  # Create users
    user_ids[user['username']] = user['id']  # Add user id to list

cohort_names = []
for subject_name in subjects.keys():
    subject_data = web.get_subject(subject_name)
    if subject_data is None:
        continue
    for cohort_data in subject_data.cohort_set.all():
        cohort_names.append(cohort_data.name)

cohort_ids = {}
for cohort in moodle_api.get_cohorts(moodle_token, cohort_names):
    cohort_ids[cohort['idnumber']] = cohort['id']

cohort_members = {}
for cohort in moodle_api.get_cohort_members(moodle_token, cohort_ids.values()):
    cohort_members[cohort['cohortid']] = cohort['userids']

cohort_new_members = []
for subject_name in subjects.keys():
    subject = web.get_subject(subject_name)
    if subject is None:
        continue  # Subject does not exist, continue to next entry
    teachers = subjects[subject_name]
    for cohort_data in subject.cohort_set.all():
        if cohort_data.name not in cohort_ids:
            continue
        cohort_id = cohort_ids[cohort_data.name]
        members = cohort_members[cohort_id]
        for user_name in teachers:
            user_id = user_ids[user_name]
            if user_id in members:
                continue
            cohort_new_members.append({
                'cohort_id': cohort_id,
                'user_id': user_id
            })

moodle_api.cohort_add_members(moodle_token, cohort_new_members)

