import web
import helpers as Help
import models as Model

class Index:

    def GET(self):

        render = web.template.render('templates', base='layout')
        data = Help.data

        data.title = 'News Map'
        data.css = 'index.css'
        data.js = 'index.js'

        locations = Model.Location.between('2017/10/01', '2017/10/10')

        for loc in locations:
            loc.top = '%f%%' % (100 - ((90 + loc.lat) / 1.8))
            loc.left = '%f%%' % ((180 + loc.lng) / 3.6)

        data.locations = locations

        return Help.Render.index(data)
