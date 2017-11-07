import helpers as Help
import arrow

class Location:

    @staticmethod
    def for_article(article_id):

        db = Help.DB.connect()

        params = {'article_id': article_id}

        return db.select('locations', params, where='article_id = $article_id').list()

    @staticmethod
    def for_articles(article_ids):

        db = Help.DB.connect()
        res = []

        for article_id in article_ids:

            params = {'article_id': article_id}
            locs = db.select('locations', params, where='article_id = $article_id').list()
            for loc in locs:
                res.append(loc)

        return res

    @staticmethod
    def between(start_date, end_date):

        db = Help.DB.connect()

        params = {'start': start_date, 'end': end_date}
        locations = db.select('locations', params, where='pub_date >= $start AND pub_date <= $end').list()

        return locations
