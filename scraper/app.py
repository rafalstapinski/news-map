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

            location = geocode(keyword['value'])

            print location
            print

            if location['country']:

                country = db.select('countries',
                    vars = {'name': location['country']},
                    where = 'name = $name'
                ).first()

                if country:
                    country_id = country.id

                else:
                    try:

                        country = geocode(location['country'])

                        country_id = db.insert('countries',
                            name = country['country'],
                            lat = country['lat'],
                            lng = country['lng']
                        )

                    except Exception, e:
                        print article_id, title, e
                        continue


            if location['level_1']:

                level_1 = db.select('level_1',
                    vars = {'name': location['level_1']},
                    where = 'name = $name'
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
                            name = level_1['level_1'],
                            lat = level_1['lat'],
                            lng = level_1['lng']
                        )

                    except Exception, e:
                        print article_id, title, e
                        continue

            if location['level_2']:

                level_2 = db.select('level_2',
                    vars = {'name': location['level_2']},
                    where = 'name = $name'
                ).first()

                if level_2:
                    level_2_id = level_2.id

                else:
                    try:

                        level_2 = geocode(location['level_2'])

                        level_2_id = db.insert('level_2',
                            name = level_2['level_2'],
                            lat = level_2['lat'],
                            lng = level_2['lng']
                        )

                    except Exception, e:
                        print article_id, title, e
                        continue


            if location['locality']:

                locality = db.select('locality',
                    vars = {'name': location['locality']},
                    where = 'name = $name'
                ).first()

                if locality:
                    locality_id = locality.id

                else:
                    try:

                        locality = geocode(location['locality'])

                        locality_id = db.insert('locality',
                            name = locality['locality'],
                            lat = locality['lat'],
                            lng = locality['lng']
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


    # if exists is None:
    #
    #     article_id = db.insert('articles',
    #         title=title,
    #         summary=summary,
    #         web_url=web_url,
    #         pub_date=pub_date
    #     )
    #
    #     for keyword in article['keywords']:
    #         if keyword['name'] == 'glocations':
    #             params = {
    #                 'address': keyword['value'],
    #                 'key': Config.get('Geocoding/api_key')
    #             }
    #             r = requests.get(Config.get('Geocoding/base_url'), params).json()
    #
    #             try:
    #                 # why is the NYT tagging the USSR in 2017
    #                 res = r['results'][0]
    #             except:
    #                 continue
    #
    #             country_name = None
    #             std_country_name = None
    #             country_lat = None
    #             country_lng = None
    #
    #             for comp in res['address_components']:
    #                 if 'country' in comp['types']:
    #                     country_name = comp['long_name']
    #                     break
    #
    #             if country_name is not None:
    #
    #                 country = db.select('countries', dict(name=country_name), where='name=$name').first()
    #
    #                 if country is not None:
    #
    #                     std_country_name = country.standard_name
    #                     country_lat = country.lat
    #                     country_lng = country.lng
    #
    #                 else:
    #
    #                     params = {
    #                         'address': country_name,
    #                         'key': Config.get('Geocoding/api_key')
    #                     }
    #
    #                     c = requests.get(Config.get('Geocoding/base_url'), params).json()
    #
    #                     try:
    #                         country = c['results'][0]
    #
    #                         country_lat = country['geometry']['location']['lat']
    #                         country_lng = country['geometry']['location']['lng']
    #                         std_country_name = country['formatted_address']
    #
    #                         db.insert('countries', name=country_name, lat=country_lat, lng=country_lng, standard_name=std_country_name)
    #
    #                     except:
    #                         pass
    #
    #             db.insert('locations', name=res['formatted_address'],
    #                                     latitude=res['geometry']['location']['lat'],
    #                                     longitude=res['geometry']['location']['lng'],
    #                                     pub_date=pub_date,
    #                                     article_id=article_id,
    #                                     country=std_country_name,
    #                                     country_lat=country_lat,
    #                                     country_lng=country_lng)
