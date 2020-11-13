import os.path
import time
import json
from typing import Text
import cherrypy
import requests

class Frontend(object):
    @cherrypy.expose
    def index(self):
        return open('./index.html')

    @cherrypy.expose
    def generate(self, text = 'I love sushi'):
        url = 'http://localhost:8081/anns'
        if cherrypy.request.body:
            body = json.loads(cherrypy.request.body.read())
            text = body['text']
            
        # The parameters we wish to send
        json_in = {
            "text": text
        }

        # Set the headers for the request
        headers = {'content-type': 'application/json'}

        # Post the request
        json_out = requests.post(url, data=json.dumps(json_in), headers=headers)

        # Retrieve the JSON of the Output
        return json_out

if __name__ == '__main__':
    
    # A note that the service has started
    print("Starting front end rest service...")

    # A default configuration
    config = {'server.socket_host': '0.0.0.0'}
    cherrypy.config.update(config)

    # Update the configuration to your host
    cherrypy.config.update({'server.socket_port': 8082})
    # cherrypy.config.update({'server.socket_host': 'dickens.seas.upenn.edu', 'server.socket_port': 4049})
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
       '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './js'
        },
    }

    # Start the service
    cherrypy.quickstart(Frontend(), '/', conf)