import os.path
import time
import json
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
def outputToJSON(string):
    """Converting the output of your annotation service to JSON"""
    # Annotate the input
    docs = model(string)

    # Create the JSON Output
    annotation_res = {}

    for token in docs:
        annotation_res[token.text] = token.pos_

    json_output = {
        "service": "spacy-pos",
        "result": annotation_res
    }

    return json.dumps(json_output)

class Annotation(object):
    @cherrypy.expose
    def index(self):
        return '''
                <form action="getText" method="GET">
                Text:
                <input type="text" name="text" size="50"/>
                <input type="submit" />
                </form>
               '''

    @cherrypy.expose
    def getText(self, text=None):
        # CherryPy passes all GET and POST variables as method parameters.
        # It doesn't make a difference where the variables come from, how
        # large their contents are, and so on.
        #
        # You can define default parameter values as usual. In this
        # example, the "name" parameter defaults to None so we can check
        # if a name was actually specified.

        if text:
            #if text is presented, we generated its corresponding annotation
            print("Result: %s" %outputToJSON(text))
            return outputToJSON(text)
        else:
            if text is None:
                # No text is specified
                return 'Please enter your text <a href="./">here</a>.'

if __name__ == '__main__':
    
    # A note that the service has started
    print("Starting rest service...")

    # A default configuration
    config = {'server.socket_host': '0.0.0.0'}
    cherrypy.config.update(config)

    # Update the configuration to your localhost:8081
    cherrypy.config.update({'server.socket_port': 8081})

    # Start the service
    cherrypy.quickstart(Annotation(), '/')