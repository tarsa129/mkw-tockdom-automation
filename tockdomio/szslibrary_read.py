import requests
from constants import *

def do_szslibrary_query(base_params):
    headers = {
        'User-Agent': SZSLIBRARY_API_KEY,
    }

    try:
        response = requests.get(SZSLIBRARY_API, headers=headers, params=base_params)
        return response.json()
    except:
        return None


def get_by_wbz_id(wbz_id):
    base_params = {
        "id": wbz_id
    }

    return do_szslibrary_query(base_params)

def get_image_from_id(image_id):
    image_id = str(image_id)
    headers = {
        'User-Agent': SZSLIBRARY_API_KEY,
    }

    url = f"{SZSLIBRARY_THUMBNAIL}{image_id[-2:]}/{image_id}.jpg"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return None
        return response.raw
    except Exception as e:
        print(e)
        return None