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
def outputToJSON(data):
    """Converting the output of your annotation service to JSON. In this case, our service is POS Tagging"""

    string = data['text']
    
    # Annotate the Input
    docs = model(string)

    # Complete the JSON Output
    annotation_pos = {}
    annotation_ner = {}

    # Load in PoS Annotations
    for token in docs:
        annotation_pos[token.text] = token.pos_

    # Load in NER Annotations
    for token in docs:
        annotation_ner[token.text] = token.ent_type_  

    json_output = {
        "PoS": annotation_pos,
        "NER": annotation_ner

    }

    return json_output

class Annotation(object):
    @cherrypy.expose
    def index(self):
        print("Currently not available")
        return 'Currently not available'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def anns(self, **params):
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
            useJSON=False
            print("\nReading Parameters from the URL")

        if useJSON:
            para = cherrypy.request.params
            if len(para) != 0:
                print("\nOverwrite JSON with Parameters (HTTP is priority)")
                data = para
       
        result = outputToJSON(data) 
        print(result)
        return result

if __name__ == '__main__':
    
    # A note that the service has started
    print("Starting rest service...")

    # A default configuration
    config = {'server.socket_host': '0.0.0.0'}
    cherrypy.config.update(config)

    # Update the configuration to your localhost:8081
    #cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.config.update({'server.socket_host': 'dickens.seas.upenn.edu', 'server.socket_port': 8099, 'cors.expose.on': True})

    # Start the service
    cherrypy.quickstart(Annotation(), '/')