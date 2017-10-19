import helpers as Help

class Location:

    @staticmethod
    def for_article(article_id):

        db = Help.DB.connect()

        params = {'article_id': article_id}

        return db.select('locations', params, where='article_id = $article_id').list()

    @staticmethod
    def for_articles(article_ids):

        db = Help.DB.connect()
        res = {}

        for article_id in article_ids:

            params = {'article_id': article_id}
            res[str(article_id)] =  db.select('locations', params, where='article_id = $article_id').list()

        return res
