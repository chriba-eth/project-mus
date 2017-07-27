import webapp2
import os
import jinja2
import json
import urllib2
import re

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

        genre_list = SongInfo(self.request.get('artist'))
        genre1 = " "
        genre = genre_list[0]
        genre = genre.split('mu')
        #genre = genre.split('|')
        genre = genre[0]
        if len(genre_list) > 1:
            genre1 = genre_list
            genre1 = genre1[1]
            genre1 = genre1.split('mu')
            genre1 = genre1[0]





        region = self.request.get('region')

        search_response = youtube.search().list(
            q= region + genre + genre1,
            part= "id, snippet",
            type = "video",
            videoDuration = "short",
            videoEmbeddable = "true",
            #relevanceLanguage = self.request.get('language'),
            videoCategoryId = "10",
            #regionCode = "FR"
            maxResults=1,
          ).execute()
        #videos = []
        #for response in search_response['items']:
        #    video = {
        #        'vidId':response['id']['videoId'],
        #        'title':response['snippet']['title']
        #    }
        #    videos.append(video)
            #    }
        vid_id = search_response['items'][0]['id']['videoId']

        title = search_response['items'][0]['snippet']['title']

        #video = {
            #'vidId':search_response['items'][0]['id']['videoId'],
            #'title':search_response['items'][0]['snippet']['title']
        #}
        #videos.append(video)

        result_vars = {
            'artist' :self.request.get('artist'),
            'region' : self.request.get('region'),
            'search_response' : search_response,
            'vidId':vid_id,
            'title':title,
            'genre':genre,
            'genre1':genre1,


            #'videos':videos

        }
        template = jinja_environment.get_template("templates/home.html")
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
def SongInfo(artist):
    name_artist = artist
    artist = artist.title().replace(' ', '_')
    f = urllib2.urlopen('https://en.wikipedia.org/w/api.php?action=query&titles=' + artist + '&prop=revisions&rvprop=content&format=json')
    dictionary = json.load(f)
    pages = dictionary['query']['pages']
    page_text = pages.values()[0]['revisions'][0]['*']
    print page_text.encode('utf-8')
    m = re.search(r'[g|G]enre\s+=\s*{{([^}]+)}}', page_text, flags=re.MULTILINE) #Grabs multiple genre artists
    if not m:
        m = re.search(r'[g|G]enre\s*=\s*(\[\[[^\]]+\]\])', page_text, flags=re.MULTILINE)
        #grabs single genre artists
    text = m.group(1)
    text = text.replace('[[',']]')
    text_genre = text.split(']]')
    actual_genres = []
    for (i, genre) in enumerate(text_genre):
        if i % 2 == 1:
            actual_genres.append(genre)

    return actual_genres




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', ResultsHandler),
    ('/login', LoginHandler)
], debug=True)
