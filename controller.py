from gpiocontroller import GPIOController
import web
import json

urls = (
  '/an', 'anControl',
  '/aus', 'ausControl',
  '/distance', 'distanceControl',
  '/', 'indexControl',
  '/vor', 'vorControl',
  '/links', 'linksControl',
  '/rechts', 'rechtsControl',
  '/zurueck', 'zurueckControl',
  '/modus/(.+)', 'modusControl'
  
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
    d0 = b.distanzVorneLinks();
    d1 = b.distanzVorneRechts();
    d2 = b.distanzHinten();
    distances = [{'name':'vorne links','distance':d0},
                 {'name':'vorne rechts', 'distance':d1},
                 {'name':'hinten', 'distance':d2}]
    web.header('Content-Type', 'application/json')
    return json.dumps(distances)

class indexControl:
  def GET(self):
    raise web.seeother('/static/index.html')

class vorControl:
  def GET(self):
    cors()
    b.vor()

class linksControl:
  def GET(self):
    cors()
    b.links()

class rechtsControl:
  def GET(self):
    cors()
    b.rechts()

class zurueckControl:
  def GET(self):
    cors()
    b.zurueck()

class modusControl:
  def GET(self, modus):
    cors();
    if modus == 'bremsassistent':
      b.bremsassistent()
    elif modus == 'automatik':
      b.automatik()
    else:
      b.manuell()

def cors():
  web.header('Access-Control-Allow-Origin',      '*')
  web.header('Access-Control-Allow-Credentials', 'true')

if __name__ == "__main__":
  app.run()
