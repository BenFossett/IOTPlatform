import requests
from flask import session

from main import app



def get_api_url(endpoint):
    return "http://{}:{}{}".format(app.config['API_HOSTNAME'], app.config['API_PORT'], endpoint)


def get_user_id():
    # TODO: remove once login functionality has been made
    session['user_id'] = 'user_id_1'
    if "user_id" in session:
        return session['user_id']
    return None


def get_user_houses():
    r = requests.get(get_api_url('/user/{}/houses'.format(get_user_id())))
    print(r.content)
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['houses']


def get_user_default_rooms():
    r = requests.get(get_api_url('/house/{}/rooms'.format(get_user_houses()[0]["house_id"])))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['rooms']
