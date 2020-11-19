import os.path
import time
import json
from typing import Text
import cherrypy
import spacy

# Load your annotation model here
model = spacy.load("en_core_web_sm")

# Make sure your model is successfully loaded
if not model:
    print('model loading failed')
else:
    print("model loaded")

# Write a function that takes an input(string/JSON) and returns a JSON output
def TokenizeToJSON(data):
    """Converting the output of your annotation service to JSON. In this case, our service is POS Tagging"""

    string = data['text']
    
    # Annotate the Input
    docs = model(string)

    # Complete the JSON Output
    annotation_token = []

    # Load in Tokenizations
    for token in docs:
        annotation_token.append(token.text)

    json_output = {
        "Tokens": annotation_token
    }

    return json_output

# Write a function that takes an input(string/JSON) and returns a JSON output
def PoSToJSON(data):
    """Converting the output of your annotation service to JSON. In this case, our service is POS Tagging"""

    string = data['text']
    
    # Annotate the Input
    docs = model(string)

    # Complete the JSON Output
    annotation_pos = {}

    # Load in PoS Annotations
    for token in docs:
        annotation_pos[token.text] = token.pos_

    json_output = {
        "PoS": annotation_pos,
    }

    return json_output

class Annotation(object):
    @cherrypy.expose
    def index(self):
        return open('../frontend/index.html')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def pos(self, **params):
        # CherryPy passes all GET and POST variables as method parameters.
        # It doesn't make a difference where the variables come from, how
        # large their contents are, and so on.
        #
        # You can define default parameter values as usual. In this
        # example, the "name" parameter defaults to None so we can check
        # if a name was actually specified.

        try:
            data = cherrypy.request.json
            useJSON = True
            print("\nReading JSON Docs from Request")

        except:
            data = cherrypy.request.params
            print(data)
            useJSON = False
            print("\nReading Parameters from the URL")

        if useJSON:
            para = cherrypy.request.params
            if len(para) != 0:
                print("\nOverwrite JSON with Parameters (HTTP is priority)")
                data = para
       
        result = PoSToJSON(data) 
        print(result)
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tokenize(self, **params):
        # CherryPy passes all GET and POST variables as method parameters.
        # It doesn't make a difference where the variables come from, how
        # large their contents are, and so on.
        #
        # You can define default parameter values as usual. In this
        # example, the "name" parameter defaults to None so we can check
        # if a name was actually specified.

        try:
            data = cherrypy.request.json
            useJSON = True
            print("\nReading JSON Docs from Request")

        except:
            data = cherrypy.request.params
            print(data)
            useJSON = False
            print("\nReading Parameters from the URL")

        if useJSON:
            para = cherrypy.request.params
            if len(para) != 0:
                print("\nOverwrite JSON with Parameters (HTTP is priority)")
                data = para
       
        result = TokenizeToJSON(data) 
        print(result)
        return result

if __name__ == '__main__':
    
    # A note that the service has started
    print("Starting rest service...")

    # A default configuration
    config = {'server.socket_host': '0.0.0.0'}
    cherrypy.config.update(config)

    # Update the configuration to your host
    cherrypy.config.update({'server.socket_port': 8081})
    
    # cherrypy.config.update({'server.socket_host': 'dickens.seas.upenn.edu', 'server.socket_port': 4049})
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
       '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '../frontend/js'
        },
    }

    # Start the service
    cherrypy.quickstart(Annotation(), '/', conf)