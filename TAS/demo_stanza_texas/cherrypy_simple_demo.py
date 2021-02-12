import os.path
import time
import json
from typing import Text
import cherrypy
import stanza
import texas as tx
import spacy_udpipe

# TODO: LRU Cache
# models = {"stanza":{}, "spacy":{} }
# models[stanza] = {"en":None, "es": None …}
# stanza_models = {"en":None, "es": None …}
# stanza_models["en"] = stanza.Pipeline("en")

# Load your annotation model here
print("Initialization starts")

model_lang_map = {}

stanza_en = stanza.Pipeline('en')
stanza_zh = stanza.Pipeline('zh')
stanza_es = stanza.Pipeline('es')

# TODO udpipe_en = spacy_udpipe.load("en")
# TODO udpipe_zh = spacy_udpipe.load("zh")
# TODO udpipe_es = spacy_udpipe.load("es")

model_lang_map["stanza"] = {"eng": stanza_en, "cmn": stanza_zh, "spa": stanza_es}
# TODO model_lang_map["spacy"] = {}
# TODO model_lang_map["udpipe"] = {}


# Define the functions to read outputs from stanza
def get_tokens_stanza(docs):
    tokens = [token.text for sentence in docs.sentences for token in sentence.tokens]
    
    return tokens

def get_sents_stanza(docs):
    end_pos = []
    id = 0
    for sentence in docs.sentences:
        id += len(sentence.tokens)
        end_pos.append(id)

    return end_pos

for package_key in model_lang_map:
    for lang_key in model_lang_map[package_key]:
        if not model_lang_map[package_key][lang_key]:
            print("Initialization fails!")
            break

################################ CherryPy Layer ################################

# Write a function that takes an input(string/JSON) and returns a TexAS object as output
def load2TexAS(data):
    """
    Converting the output of your annotation service to TexAS.
    In this case, our service is tokenization and sentence separation
    """
    # Collect the data
    string = data['text']
    lang = data['lang']
    package = data['package']
    
    print(string, lang, package)
    # Initialize the TexAS document
    mydoc = tx.Document(string)
    mydoc.meta().set("authors","hegler,yiwen,celine,yuqian")
    mydoc.date().setTimestamp("2021-01-19T14:44")

    model = model_lang_map[package][lang]
    docs = model(string)
 
    end_pos = get_sents_stanza(docs)
    tokens = get_tokens_stanza(docs)

    mydoc.setTokenList(tokens, indexed=True)
    mydoc.views().get("TOKENS").meta().set("generator", "stanza")
    mydoc.views().get("TOKENS").meta().set("model", package + "-" + lang )
    mydoc.setSentenceList(end_pos)

    myTabView = tx.UITabularView(mydoc)
    return myTabView.HTML().replace("\n", "").replace('\"', '')

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
       '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '../frontend/css'
        },
    }

    # Start the service
    cherrypy.quickstart(Annotation(), '/', conf)
