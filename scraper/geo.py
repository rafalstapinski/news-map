from config import Config
import requests
import json


class GeoCodeError(Exception):

    def __init__(self, message):

        super(GeoCodeError, self).__init__(message)


def geocode(q):

    params = {
        'address': q,
        'key': Config.get('Geocoding/api_key')
    }

    r = requests.get(Config.get('Geocoding/base_url'), params).json()

    if r['status'] != 'OK':

        raise GeoCodeError('GeoCode API Rate Limit')

    if len(r['results'] < 1):

        raise GeoCodeError('No results found. This is probably the USSR. ')

    country = None
    level_1 = None
    level_2 = None
    locality = None

    for comp in r['results'][0]['address_components']:

        # if 'country' in comp['types']:
        #     country =
        if comp is None:
            continue

        if 'country' in comp['types']:
            country = comp['long_name']
        elif 'administrative_area_level_1' in comp['types']:
            level_1 = comp['long_name']
        elif 'administrative_area_level_2' in comp['types']:
            level_2 = comp['long_name']
        elif 'locality' in comp['types']:
            locality = comp['long_name']


    lat = r['results'][0]['geometry']['location']['lat']
    lng = r['results'][0]['geometry']['location']['lng']

    return {
        'country': country,
        'level_1': level_1,
        'level_2': level_2,
        'locality': locality,
        'lng': lat,
        'lng': lng
    }
