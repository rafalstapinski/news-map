import json
import web

class Write:

    @staticmethod
    def error(error):
        web.header('Content-type', 'application/json')
        return json.dumps({'error': error})

    @staticmethod
    def message(message):
        web.header('Content-type', 'application/json')
        return json.dumps({'message': message})

    @staticmethod
    def object(name, val):
        web.header('Content-type', 'application/json') 
        return json.dumps({name: val})
