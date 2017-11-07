import time
import arrow
import helpers as Help

class Article:

    @staticmethod
    def between(start_date, end_date):

        db = Help.DB.connect()

        params = {'start': start_date, 'end': end_date + 86400}
        articles = db.select('articles', params, where='pub_date >= $start AND pub_date <= $end').list()

        return articles
