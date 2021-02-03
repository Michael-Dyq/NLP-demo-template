import os.path
import time
import json
from typing import Text
import cherrypy
import stanza
import texas as tx

# download English, Chinese, and Spanish model (takes a while)
# stanza.download('en')
# stanza.download('zh')
# stanza.download('es')

# Load your annotation model here
print("Initialization starts")

# TODO: LRU Cache
# models = {"stanza":{}, "spacy":{} }
# models[stanza] = {"en":None, "es": None …}
# stanza_models = {"en":None, "es": None …}
# stanza_models["en"] = stanza.Pipeline("en")

# initialize English neural pipeline
nlp_en = stanza.Pipeline('en')

# initialize Chinese neural pipeline
nlp_zh = stanza.Pipeline('zh')

# initialize Spanish neural pipeline
nlp_es = stanza.Pipeline('es')

if not nlp_en or not nlp_es or not nlp_zh:
    print("Initialization fails!")

################################

# Write a function that takes an input(string/JSON) and returns a TexAS object as output
def load2TexAS(data):
    """
    Converting the output of your annotation service to TexAS.
    In this case, our service is tokenization and sentence separation
    """
    # Collect the data
    string = data['text']
    lang = data['lang']
    
    # # Initialize the TexAS document
    mydoc = tx.Document(string)
    mydoc.meta().set("authors","hegler,yiwen,celine,yuqian")
    mydoc.date().setTimestamp("2021-01-19T14:44")

    docs = None
    if lang == "eng":
        docs = nlp_en(string)

    elif lang == "cmn":
        docs = nlp_zh(string)
    
    elif lang == "spa":
        docs = nlp_es(string)
 
    end_pos = []
    id = 0
    for sentence in docs.sentences:
        id += len(sentence.tokens)
        end_pos.append(id)
    
    tokens = [token.text for sentence in docs.sentences for token in sentence.tokens]

    # # Conduct the tokenization and sentence separation
    mydoc.setTokenList(tokens)
    mydoc.setSentenceList(end_pos)

    return mydoc

class Annotation(object):
    @cherrypy.expose
    def index(self):
        return open('../frontend/index.html')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def process(self, **params):
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
       
        result = load2TexAS(data) 
        print(result)
        return result.jss()

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
