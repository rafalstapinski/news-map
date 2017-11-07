import web
import routes as Route
import helpers as Help

Index = Route.Index
Location = Route.Location
Article = Route.Article

urls = (
    '/',            'Index',
    # '/locations',   'Location',
    '/articles',    'Article'
)

Help.Config.set()
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
