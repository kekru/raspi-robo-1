from gpiocontroller import GPIOController
import web
import json

urls = (
  '/an', 'anControl',
  '/aus', 'ausControl',
  '/distance', 'distanceControl',
  '/', 'indexControl'
)

b = GPIOController()
#while 1:
#  b.an()
#  b.aus()

app = web.application(urls, globals())
#web.header('Access-Control-Allow-Origin',      '*')
#web.header('Access-Control-Allow-Credentials', 'true')

class anControl:
  def GET(self):
    cors()
    b.an()

class ausControl:
  def GET(self):
    cors()
    b.aus()

class distanceControl:
  def GET(self):
    cors()
    d0 = b.distanz(18, 24);
    distances = [{'name':'vorne','distance':d0}]
    web.header('Content-Type', 'application/json')
    return json.dumps(distances)

class indexControl:
  def GET(self):
    raise web.seeother('/static/index.html')

def cors():
  web.header('Access-Control-Allow-Origin',      '*')
  web.header('Access-Control-Allow-Credentials', 'true')

if __name__ == "__main__":
  app.run()
