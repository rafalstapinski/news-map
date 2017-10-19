import time
import arrow
import helpers as Help

class Article:

    @staticmethod
    def between(start_date, end_date):

        start = arrow.get(start_date).timestamp
        end = arrow.get(end_date).timestamp

        db = Help.DB.connect()

        params = {'start': start, 'end': end}
        articles = db.select('articles', params, where='pub_date >= $start AND pub_date <= $end').list()

        return articles
