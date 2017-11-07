import web
import routes as Route
import helpers as Help

from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = "/etc/letsencrypt/live/newsmap.stapinski.co/fullchain.pem"
CherryPyWSGIServer.ssl_private_key = "/etc/letsencrypt/live/newsmap.stapinski.co/privkey.pem"

Index = Route.Index
Location = Route.Location

urls = (
    '',            'Index',
    '/locations',   'Location'
)

Help.Config.set()
app = web.application(urls, globals())
application = app.wsgifunc()
