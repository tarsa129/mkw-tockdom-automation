import requests
from constants import *

def do_szslibrary_query(base_params):
    headers = {
        'User-Agent': SZSLIBRARY_API_KEY,
    }

    response = requests.get(SZSLIBRARY_API, headers=headers, params=base_params)
    return response.json()

def get_by_wbz_id(wbz_id):
    base_params = {
        "id": wbz_id
    }

    return do_szslibrary_query(base_params)