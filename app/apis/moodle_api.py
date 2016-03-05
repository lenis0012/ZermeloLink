import urllib
import urllib2
import json

moodle_token_url = "login/token.php"
moodle_api_service = "webservice/rest/server.php"
moodle_api_user_format = "users[{0}][{1}]={2}&"
moodle_api_value_format = "values[{0}]={1}&"
moodle_api_cohortid_format = "cohortids[{0}]={1}&"
moodle_api_cohortidnr_format = "cohortidnumbers[{0}]={1}&"
moodle_api_member_format = "members[{0}][{1}][{2}]={3}&"


# Set the base url for moodle
def base_url(url):
    global moodle_base_url
    moodle_base_url = url


# Get the user's authentication token
def get_user_token(user, password, service='zlink'):
    global moodle_base_url
    params = {
        'username': user,
        'password': password,
        'service': service
    }

    url = moodle_base_url + moodle_token_url + "?" + urllib.urlencode(params)
    request = urllib2.urlopen(url)  # Request token from moodle
    return json.load(request)


# Get list of existing users
def get_users(user_token, users):
    post_data = "field=username&"
    for i in range(len(users)):
        user = users[i]
        post_data += moodle_api_value_format.format(i, user)
    post_data = post_data[:len(post_data)-1]  # Remove last character
    return execute_api_function(user_token, 'core_user_get_users_by_field', post_data)


def get_cohorts(user_token, cohort_names):
    post_data = ""
    for i in range(len(cohort_names)):
        cohort_name = cohort_names[i]
        post_data += moodle_api_cohortidnr_format.format(i, cohort_name)
    post_data = post_data[:len(post_data)-1]  # Remove last character
    return execute_api_function(user_token, 'core_cohort_get_cohorts_by_idnumber', post_data)


# Get members of cohorts
def get_cohort_members(user_token, cohort_ids):
    post_data = ""
    for i in range(len(cohort_ids)):
        cohort_id = cohort_ids[i]
        post_data += moodle_api_cohortid_format.format(i, cohort_id)
    post_data = post_data[:len(post_data)-1]  # Remove last character
    return execute_api_function(user_token, 'core_cohort_get_cohort_members', post_data)


def cohort_add_members(user_token, members):
    if len(members) <= 0:
        return
    post_data = ""
    for i in range(len(members)):
        member = members[i]
        post_data += moodle_api_member_format.format(i, 'cohorttype', 'type', 'id')
        post_data += moodle_api_member_format.format(i, 'cohorttype', 'value', member['cohort_id'])
        post_data += moodle_api_member_format.format(i, 'usertype', 'type', 'id')
        post_data += moodle_api_member_format.format(i, 'usertype', 'value', member['user_id'])
    post_data = post_data[:len(post_data)-1]  # Remove last character
    return execute_api_function(user_token, 'core_cohort_add_cohort_members', post_data)


# Create a set of users
def create_users(user_token, users):
    if len(users) <= 1:
        return []  # No users to be created
    post_data = ""
    # Append each user to post data
    for i in range(len(users)):
        user = users[i]
        post_data += moodle_api_user_format.format(i, 'username', user['code'])
        post_data += moodle_api_user_format.format(i, 'createpassword', '1')
        post_data += moodle_api_user_format.format(i, 'firstname', user['firstName'])
        post_data += moodle_api_user_format.format(i, 'lastname', user['lastName'])
        post_data += moodle_api_user_format.format(i, 'email', user['email'])
        post_data += moodle_api_user_format.format(i, 'auth', 'manual')
        post_data += moodle_api_user_format.format(i, 'middlename', user['prefix'])
    post_data = post_data[:len(post_data)-1]  # Remove last character
    return execute_api_function(user_token, 'core_user_create_users', post_data)


# Execute an api method
def execute_api_function(user_token, function_name, function_data):
    global moodle_base_url
    params = {
        'wstoken': user_token,
        'wsfunction': function_name,
        'moodlewsrestformat': 'json'
    }

    url = moodle_base_url + moodle_api_service + "?" + urllib.urlencode(params)  # create url
    request = urllib2.Request(url, function_data)  # create POST request
    response = urllib2.urlopen(request)  # call post request
    return json.load(response)
