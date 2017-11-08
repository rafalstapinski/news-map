import time
import helpers as Help

class Article:

    @staticmethod
    def between(start_date, end_date):

        db = Help.DB.connect()

        params = {
            'start_date': start_date,
            'end_date': end_date + 86400
        }

        countries = db.query(
            '''
                SELECT *
                FROM glocations
                INNER JOIN articles
                ON glocations.article_id = articles.id
                INNER JOIN countries
                ON glocations.country = countries.id
                WHERE (
                    glocations.pub_date >= $start_date
                    AND
                    glocations.pub_date <= $end_date
                )
            ''',
            vars = params
        ).list()

        return {
            'countries': countries
        }
