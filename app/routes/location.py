import web

import validators as Validate
import models as Model

class Location:

    def GET(self):

        data = Validate.Location.GET(web.input())

        if not data.is_valid:
            return Help.Write.error('Invalid dates. ')

        locations = Model.Location.between(data.start_date, data.end_date)

        res = []
        track = []

        for location in locations:
            if location.name not in track:
                track.append(location.name)
                l = {
                    'name': location.name,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'country': location.country,
                    'country_lat': location.country_lat,
                    'country_lng': location.country_lng,
                    'radius': 10
                }
                res.append(l)
            else:
                res[track.index(location.name)]['radius'] += 1

        return Help.Write.object('locations', res)
