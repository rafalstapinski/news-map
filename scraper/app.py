from scraper import Scraper
from config import Config
import web
import json
import requests
import arrow

# for year in range(2000, 2018):
#     for month in range(1, 13):
#         s = Scraper(year, month)
#         print s.gloc

Config.set()

s = Scraper(2017, 9)

db = web.database(dbn=Config.get('DB/dbn'),
                    db=Config.get('DB/db'),
                    user=Config.get('DB/user'),
                    pw=Config.get('DB/pw'),
                    host=Config.get('DB/host')
                    )


for article in s.gloc:

    if 'abstract' in article:
        summary = article['abstract']
    elif 'lead_paragraph' in article:
        summary = article['lead_paragraph']
    elif 'snippet' in article:
        summary = article['snippet']
    else:
        summary = None

    web_url = article['web_url']
    title = article['headline']['main']
    pub_date = arrow.get(article['pub_date']).timestamp

    exists = db.select('articles', dict(web_url=web_url), where='web_url=$web_url').first()

    if exists is None:
        article_id = db.insert('articles', title=title, summary=summary, web_url=web_url, pub_date=pub_date)

        for keyword in article['keywords']:
            if keyword['name'] == 'glocations':
                params = {
                    'address': keyword['value'],
                    'key': Config.get('Geocoding/api_key')
                }
                r = requests.get(Config.get('Geocoding/base_url'), params).json()

                try:
                    # why is the NYT tagging the USSR in 2017
                    res = r['results'][0]
                except:
                    continue

                db.insert('locations', name=res['formatted_address'],
                                        lat=res['geometry']['location']['lat'],
                                        lng=res['geometry']['location']['lng'],
                                        article_id=article_id)
