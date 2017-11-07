from data import data

class Location:

    @staticmethod
    def GET(i):

        if i.get('start_date') is None or i.get('end_date') is None:
            data.is_valid = False
            return data

        data.start_date = i.get('start_date')
        data.end_date = i.get('end_date')
        data.is_valid = True

        return data
