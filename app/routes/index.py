import web
import helpers as Help
import models as Model

class Index:

    def GET(self):

        render = web.template.render('templates', base='layout')
        data = Help.data

        data.title = 'News Map'
        data.css = 'index.css'
        scripts = [
                    '//cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js',
                    '//cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js',
                    '/static/js/lib/datamaps/datamaps.world.min.js',
                    '/static/js/index.js'
        ]
        data.js = ' '.join(scripts);

        locations = Model.Location.between('2017/10/01', '2017/10/10')

        res = []
        countries = {}

        for loc in locations:
            if loc.country_lat is not None:
                loc.top = '%f%%' % (100 - ((90 + loc.country_lat) / 1.8))
                loc.left = '%f%%' % ((180 + loc.country_lng) / 3.6)
                res.append(loc)
                if loc.country in countries:
                    countries[loc.country][0] += 1
                else:
                    countries[loc.country] = [1, loc.top, loc.left, loc.country]

        data.locations = res
        data.c = countries

        return Help.Render.index(data)
