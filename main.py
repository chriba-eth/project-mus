import webapp2
import os
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
# class Search(ndb.model):
#
class MainHandler(webapp2.RequestHandler):
    def get(self):
        genre = self.request.get('genre')
        template_vars = {
            'genre': genre
        }
        template = jinja_environment.get_template("templates/home.html")
        self.response.write(template.render())
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
