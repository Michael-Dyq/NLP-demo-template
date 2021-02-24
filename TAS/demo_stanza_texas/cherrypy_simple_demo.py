import os.path
import time
import json
from typing import Text
import cherrypy
import texas as tx
import stanza
import spacy_udpipe
import spacy

# TODO: LRU Cache (Time to live)
# models = {"stanza":{}, "spacy":{} }
# models[stanza] = {"en":None, "es": None …}
# stanza_models = {"en":None, "es": None …}
# stanza_models["en"] = stanza.Pipeline("en")

################################ Model Loading ################################
print("Initialization starts")
model_lang_map = {}

print("Stanza model initialization starts")
stanza_en = stanza.Pipeline('en', processors='tokenize,pos,lemma,ner')
stanza_zh = stanza.Pipeline('zh', processors='tokenize,pos,lemma,ner')
stanza_es = stanza.Pipeline('es', processors='tokenize,pos,lemma,ner')
stanza_fr = stanza.Pipeline('fr', processors='tokenize,pos,lemma,ner')
stanza_de = stanza.Pipeline('de', processors='tokenize,pos,lemma,ner')
# stanza_jp = stanza.Pipeline('ja')
print("Stanza model initialization ends")

print("SpaCy model initialization starts")
spacy_en = spacy.load("en_core_web_sm")
spacy_zh = spacy.load("zh_core_web_sm")
spacy_es = spacy.load("es_core_news_sm")
# spacy_jp = spacy.load("ja_core_news_sm")
spacy_de = spacy.load("de_core_news_sm")
spacy_fr = spacy.load("fr_core_news_sm")
print("SpaCy model initialization ends")

print("UDpipe model initialization starts")
udpipe_en = spacy_udpipe.load("en")
udpipe_zh = spacy_udpipe.load("zh")
udpipe_es = spacy_udpipe.load("es")
# udpipe_jp = spacy_udpipe.load("ja")
udpipe_de = spacy_udpipe.load("de")
udpipe_fr = spacy_udpipe.load("fr")
print("UDpipe model initialization ends")

model_lang_map["spacy"] = {"eng": spacy_en, "cmn": spacy_zh, "spa": spacy_es, "fre": spacy_fr, "ger": spacy_de }
model_lang_map["stanza"] = {"eng": stanza_en, "cmn": stanza_zh, "spa": stanza_es, "fre": stanza_fr, "ger": stanza_de }
model_lang_map["udpipe"] = {"eng": udpipe_en, "cmn": udpipe_zh, "spa": udpipe_es, "fre": udpipe_fr, "ger": udpipe_de }

################################ Processor Functions ################################
# Define the functions to read outputs from STANZA
def get_services_stanza(docs):
    index = -1
    sentIndex = 0
    tokens = [] # score token objects
    nlpTokenList = [] # score token text
    nlpPOSList = []
    nlpLemmaList = []
    nlpSentenceEndPositions = []
    nlpNERList = []

    for sentence in docs.sentences:
        sentIndex+=len(sentence.tokens)
        nlpSentenceEndPositions.append(sentIndex)
        for word in sentence.words:
            index += 1
            nlpTokenList.append(word.text)
            nlpPOSList.append(word.pos)
            nlpLemmaList.append(word.lemma)
    
        for token in sentence.tokens:
            tokens.append(token)

    word_index = 0
    for idx in range(len(tokens)):
        token = tokens[idx]
        if token.ner.startswith("S-"):
            nerLabel = token.ner[2:]
            nlpNERList.append( [nerLabel, word_index] )
        if token.ner.startswith("B-"):
            start_token = word_index
            nerLabelStart = token.ner[2:]
        if token.ner.startswith("E-"):
            final_token = word_index
            nerLabelFinal = token.ner[2:]
            if nerLabelStart == nerLabelFinal:
                nlpNERList.append( [nerLabelFinal, start_token, final_token+1] )
                nerLabelStart = ""
                nerLabelFinal = ""
        word_index += len(token.words)

    return nlpTokenList, nlpSentenceEndPositions, nlpLemmaList, nlpPOSList, nlpNERList

# Define the functions to read outputs from SpaCy
def get_services_spacy(docs):
    index = -1
    sentIndex = 0
    nlpTokenList = []
    nlpPOSList = []
    nlpLemmaList = []
    nlpNerList = []
    nlpSentenceEndPositions = []

    for sentence in docs.sents:
        sentIndex+=len(sentence)
        nlpSentenceEndPositions.append(sentIndex)

    for token in docs:
        index += 1
        nlpTokenList.append(token.text)
        nlpPOSList.append(token.pos_)
        nlpLemmaList.append(token.lemma_)
        nlpNerList.append([token.ent_iob_, token.ent_type_]) # eg:[['B','NORP'],['O',''],...]
        
    # NER
    nerList = []
    word_index = 0
    start_token, inside_token, final_token = -1,-1,-1
    contin = True
    for idx in range(len(nlpNerList)):
        token_iob, token_ner = nlpNerList[idx]
        if token_iob == 'B':
            if len(nerList) == 0 and contin:
                start_token = word_index
                nerLabelStart = token_ner
                contin=False
                
            else:
                if start_token < final_token:
                    nerList.append([nerLabelStart, start_token, final_token+1])
                else:
                    nerList.append([nerLabelStart, start_token])
                start_token = word_index
                nerLabelStart = token_ner
                
        if token_iob == 'I':
            inside_token = word_index

        if token_iob == 'O':
            final_token = inside_token
                
        word_index += 1
        
    if start_token == -1:
        pass

    else:
        if start_token < final_token:
            nerList.append([nerLabelStart, start_token, final_token+1])
        else:
            nerList.append([nerLabelStart, start_token])

    return nlpTokenList, nlpSentenceEndPositions, nlpLemmaList, nlpPOSList, nerList


# Define the functions to read outputs from UDpipe
def get_services_udpipe(docs):
    index = -1
    sentIndex = 0
    nlpTokenList = []
    nlpPOSList = []
    nlpLemmaList = []
    nlpSentenceEndPositions = []

    for sentence in docs.sents:
        sentIndex+=len(sentence)
        nlpSentenceEndPositions.append(sentIndex)

    for token in docs: 
        index += 1
        nlpTokenList.append(token.text)
        nlpPOSList.append(token.pos_)
        nlpLemmaList.append(token.lemma_)

    return nlpTokenList, nlpSentenceEndPositions, nlpLemmaList, nlpPOSList


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
    mydoc.meta().set("package", package)
    mydoc.date().setTimestamp("2021-01-19T14:44")

    model = model_lang_map[package][lang]
    docs = model(string)
    
    # if "stanza" in [], make 1 request instead of 3, change to packages
    # len(tokens) = #tokens
    # len(end_pos) = #sentence
    # process(end_pos) = #tokens per sentences
    if package == "stanza":
        tokens, end_pos, lemma, pos, ner = get_services_stanza(docs)

    elif package == "spacy":
        tokens, end_pos, lemma, pos, ner = get_services_spacy(docs)

    elif package == "udpipe":
        tokens, end_pos, lemma, pos = get_services_udpipe(docs)

    else:
        print("Invalid Model. Please try again...")
        return

    mydoc.setTokenList(tokens, indexed=True)
    mydoc.views().get("TOKENS").meta().set("generator", package)
    mydoc.views().get("TOKENS").meta().set("model", package + "-" + lang )
    mydoc.setSentenceList(end_pos)
    mydoc.addTokenView("LEMMA", lemma)
    mydoc.addTokenView("POS", pos)
    
    # Extract HTML View
    myTabView = tx.UITabularView(mydoc)
    myTabView.showView("LEMMA", labelCSS=False)
    myTabView.showView("POS")
    if package == "stanza" or package == "spacy":
        mydoc.addSpanView("NER", ner)
        myTabView.showView("NER")

    # concatenate the myTabView.HTML()
    return myTabView.HTML().replace("\n", "")

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
