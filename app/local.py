import web
import routes as Route
import helpers as Help

Index = Route.Index
Location = Route.Location

urls = (
    '/',            'Index',
    '/locations',   'Location'
)

Help.Config.set()
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
