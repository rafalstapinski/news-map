import web

import validators as Validate
import models as Model

class Article:

    def GET(self):

        data = Validate.Article.GET(web.input())

        if not data.is_valid:
            return Help.Write.error('Invalid dates. ')

        print Model.Article.between(data.start_date, data.end_date)
