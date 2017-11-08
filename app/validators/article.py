from _data import data
import arrow

class Article:

    @staticmethod
    def GET(i):

        if i.get('start_date') is None or i.get('end_date') is None:
            data.is_valid = False
            return data

        print i.get('start_date'), i.get('end_date')

        start = arrow.get(i.get('start_date')).timestamp
        end = arrow.get(i.get('end_date')).timestamp

        if end > start:
            data.is_valid = False

        data.start_date = start
        data.end_date = end
        data.is_valid = True

        return data
