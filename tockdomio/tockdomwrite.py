#The purpose of this file is to communicate with the tockdom wiki.

import requests
from requests import Response
from constants import *

def get_tockdom_query(base_params, cookies=None) -> Response:
    headers = {
        'User-Agent': TOCKDOM_API_KEY
    }

    response = requests.get(TOCKDOM_API, headers=headers, params=base_params, cookies=cookies)
    return response

def post_tockdom_query(data, cookies=None, files=None):
    headers = {
        'User-Agent': TOCKDOM_API_KEY,
    }

    response = requests.post(TOCKDOM_API, headers=headers, data=data, cookies=cookies, files=files)
    return response

def get_login_token_response():
    base_params = {
        "action": "query",
        "format": "json",
        "meta": "tokens",
        "type": "login",
        "formatversion": "2"
    }
    return get_tockdom_query(base_params)

def login():
    login_response = get_login_token_response()
    login_token = login_response.json()["query"]["tokens"]["logintoken"]
    base_params = {
        "action": "login",
        "lgname": WIKI_BOT_USERNAME,
        "lgpassword": WIKI_BOT_PASSWORD,
        "lgtoken": login_token,
        "format": "json"
    }
    response = post_tockdom_query(base_params, cookies=login_response.cookies)
    return response.cookies

def get_csrf_token(cookies):
    base_params = {
        "action": "query",
        "format": "json",
        "meta": "tokens",
        "formatversion": "2"
    }
    return get_tockdom_query(base_params, cookies=cookies).json()["query"]["tokens"]["csrftoken"]

def edit_section(pageid, sectionid, section_text, edit_summary="Test Editing via API", minor=True):
    login_cookies = login()
    token = get_csrf_token(login_cookies)

    base_params = {
        "action": "edit",
        "pageid": pageid,
        "section":sectionid,
        "format": "json",
        "text": section_text,
        "summary": edit_summary,
        "token": token,
        "minor": minor,
        "bot": True
    }
    response = post_tockdom_query(base_params, cookies=login_cookies)
    return response


def upload_file(file_name, file_data):
    login_cookies = login()
    token = get_csrf_token(login_cookies)

    base_params = {
        "action": "upload",
        "filename": file_name,
        "token": token,
        "format": "json",
    }

    file = {'file': (file_name, file_data, 'multipart/form-data')}

    response = post_tockdom_query(base_params, cookies=login_cookies, files=file)
    return response