import webapp2
import os
import jinja2

from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Search(ndb.Model):
#    artist = ndb.StringProperty()
    genres = ndb.StringProperty()
    region = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        search = Search.query().fetch()
        template = jinja_environment.get_template("templates/home.html")
        template_vars = {
            'search': search
        }
#       test
        self.response.write(template.render(template_vars))

    def post(self):
        genres = self.request.get('genres')
        region = self.request.get('region')
        search = Search(genres = genres, region = region)
        region.put()
        self.redirect('/')
#
#
# class FilterHandler(webapp2.RequestHandler):
#     def get(self):
#         template =jinja_enviroment.get_template()
#         self.response.write(template.render())
#
# class PlaylistHandler(webapp2.RequestHandler):
#     def get(self):
#         template =jinja_enviroment.get_template()
#         self.response.write(template.render())
#
# class MapHandler(webapp2.RequestHandler):
#     def get(self):
#         template =jinja_enviroment.get_template()
#         self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
