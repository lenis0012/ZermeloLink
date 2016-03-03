# import mysql.connector
#
# def connect_to_moodle(user='root', password='', host='127.0.0.1', database='moodle', tbl_prefix='mdl_'):
#     global cnx
#     global prefix
#     cnx = mysql.connector.connect(user, password, host, database)
#     prefix = tbl_prefix
#
# def insert_user()
import urllib
import urllib2
import json

moodle_token_url = "login/token.php"
moodle_api_service = "webservice/rest/server.php"

# Set the base url for moodle
def base_url(url):
    global moodle_base_url
    moodle_base_url = url

# Get the user's authentication token
def get_user_token(user, password, service='moodle_mobile_app'):
    global moodle_base_url
    params = {
        'username': user,
        'password': password,
        'service': service
    }

    url = moodle_base_url + moodle_token_url + "?" + urllib.urlencode(params)
    print url
    request = urllib2.urlopen(url) # Request token from moodle
    return json.load(request)

# Create a set of users
def create_users(user_token, users):
    return execute_api_function(user_token, 'core_user_create_users', users)

# Esecute an api method
def execute_api_function(user_token, function_name, function_data):
    global moodle_base_url
    params = {
        'wstoken': user_token,
        'wsfunction': function_name,
        'moodlewsrestformat': 'json'
    }

    url = moodle_base_url + moodle_api_service + "?" + urllib.urlencode(params) # create url
    request = urllib2.Request(url, function_data) # create POST request
    response = urllib2.urlopen(request) # call post request
    return json.load(response)