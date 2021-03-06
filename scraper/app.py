from scraper import Scraper
from config import Config
from geo import geocode
import web
import json
import requests
import arrow

Config.set()

s = Scraper(2017, 11)

db = web.database(
    dbn = Config.get('DB/dbn'),
    db = Config.get('DB/db'),
    user = Config.get('DB/user'),
    pw = Config.get('DB/pw'),
    host = Config.get('DB/host')
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

    article_exists = db.select('articles',
        vars = dict(web_url = web_url),
        where = 'web_url = $web_url'
    ).first()


    if article_exists:
        continue

    article_id = db.insert('articles',
        title = title,
        summary = summary,
        web_url = web_url,
        pub_date = pub_date
    )

    for keyword in article['keywords']:

        country_id = None
        level_1_id = None
        level_2_id = None
        locality_id = None

        if keyword['name'] == 'glocations':

            print
            print keyword['value']

            try:

                location = geocode(keyword['value'])

            except Exception, e:

                print article_id, title, e
                continue

            print location
            print

            if location['country']:

                country = db.select('countries',
                    vars = {'name': location['country']},
                    where = 'country_name = $name'
                ).first()

                if country:
                    country_id = country.id

                else:
                    try:

                        country = geocode(location['country'])

                        country_id = db.insert('countries',
                            country_name = country['country'],
                            country_lat = country['lat'],
                            country_lng = country['lng']
                        )

                    except Exception, e:
                        print article_id, title, e
                        continue


            if location['level_1']:

                level_1 = db.select('level_1',
                    vars = {'name': location['level_1']},
                    where = 'level_1_name = $name'
                ).first()

                if level_1:

                    print 'level_1 already inserted', location['level_1']
                    print

                    level_1_id = level_1.id

                else:
                    try:

                        print 'geocode level_1', location['level_1']
                        print

                        level_1 = geocode(location['level_1'])

                        level_1_id = db.insert('level_1',
                            level_1_name = level_1['level_1'],
                            level_1_lat = level_1['lat'],
                            level_1_lng = level_1['lng']
                        )

                    except Exception, e:
                        print article_id, title, e
                        continue

            if location['level_2']:

                level_2 = db.select('level_2',
                    vars = {'name': location['level_2']},
                    where = 'level_2_name = $name'
                ).first()

                if level_2:
                    level_2_id = level_2.id

                else:
                    try:

                        level_2 = geocode(location['level_2'])

                        level_2_id = db.insert('level_2',
                            level_2_name = level_2['level_2'],
                            level_2_lat = level_2['lat'],
                            level_2_lng = level_2['lng']
                        )

                    except Exception, e:
                        print article_id, title, e
                        continue


            if location['locality']:

                locality = db.select('locality',
                    vars = {'name': location['locality']},
                    where = 'locality_name = $name'
                ).first()

                if locality:
                    locality_id = locality.id

                else:
                    try:

                        locality = geocode(location['locality'])

                        locality_id = db.insert('locality',
                            locality_name = locality['locality'],
                            locality_lat = locality['lat'],
                            locality_lng = locality['lng']
                        )

                    except Exception, e:
                        print article_id, title, e
                        continue


            db.insert('glocations',
                article_id = article_id,
                country = country_id,
                level_1 = level_1_id,
                level_2 = level_2_id,
                locality = locality_id,
                pub_date = pub_date
            )
