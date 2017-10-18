from config import Config
import requests
import json

class Scraper:

    def __init__(self, year, month):

        self.year = year
        self.month = month
        self.gloc = []

        self.get()
        self.sort()


    def get(self):

        url = Config.get('NYT/base_url') % (self.year, self.month)

        params = {'api-key': Config.get('NYT/api_key')}

        r = requests.get(url, params).json()

        self.response = r

    def sort(self):

        for article in self.response['response']['docs']:
            for keyword in article['keywords']:
                if keyword['name'] == 'glocations':
                    self.gloc.append(article)
                    break
