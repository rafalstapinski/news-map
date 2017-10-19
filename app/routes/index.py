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

        articles = Model.Article.between('2017/09/01', '2017/09/12')

        print articles

        data.l = ['1', 'b', 'c']

        return Help.Render.index(data)
