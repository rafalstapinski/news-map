import web

import validators as Validate
import models as Model

class Article:

    def GET(self):

        data = Validate.Article.GET(web.input())

        if not data.is_valid:
            return Help.Write.error('Invalid dates. ')

        return Help.Write.object(
            'articles', Model.Article.between(data.start_date, data.end_date)
        )
