from config import Config
import requests
import json

class RateLimitError(Exception):

    def __init__(self, message):

        super(RateLimitError, self).__init__(message)

def geocode(q):

    params = {
        'address': q,
        'key': Config.get('Geocoding/api_key')
    }

    r = requests.get(Config.get('Geocoding/base_url'), params).json()

    if r['status'] != 'OK':

        raise RateLimitError('GeoCode API Rate Limit')

    country = None
    level_1 = None
    level_2 = None
    locality = None

    for comp in r['results'][0]['address_components']:

        # if 'country' in comp['types']:
        #     country =
        if comp is None:
            continue
