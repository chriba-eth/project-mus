import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from apiclient.discovery import build


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.


DEVELOPER_KEY = "AIzaSyBUemp0rfndbXxXm4hM2MzSGm-b0PxlVH4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"






jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/home.html")

        current_user= users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url= users.create_login_url('/')


        template_vars = {
        'current_user':current_user,
        'logout_url': logout_url,
        'login_url': login_url,
        }
        self.response.write(template.render(template_vars))

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/login.html")

        current_user= users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url= users.create_login_url('/')


        template_vars = {
        'current_user':current_user,
        'logout_url': logout_url,
        'login_url': login_url,
        }
        self.response.write(template.render(template_vars))



class ResultsHandler(webapp2.RequestHandler):
    def post(self):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=self.request.get('region') + self.request.get('artist'),
            part="id,snippet",
            type = "video",
            videoDuration = "short",
            videoEmbeddable = "true",
            maxResults=1,
          ).execute()

        result_vars = {
            'artist' :self.request.get('artist'),
            'region' : self.request.get('region'),
            'search_response' : search_response

        }
        template = jinja_environment.get_template("templates/results.html")
        self.response.write(template.render(result_vars))


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
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/login', LoginHandler)
], debug=True)
