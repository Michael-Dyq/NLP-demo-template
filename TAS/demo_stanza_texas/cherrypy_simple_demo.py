import os.path
import time
import json
from typing import Text

from typing_extensions import final
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
stanza_en = stanza.Pipeline('en', processors='tokenize,pos,lemma')
stanza_zh = stanza.Pipeline('zh', processors='tokenize,pos,lemma')
stanza_es = stanza.Pipeline('es', processors='tokenize,pos,lemma')
stanza_fr = stanza.Pipeline('fr', processors='tokenize,pos,lemma')
stanza_de = stanza.Pipeline('de', processors='tokenize,pos,lemma')
stanza_ja = stanza.Pipeline('ja', processors='tokenize,pos,lemma')
stanza_it = stanza.Pipeline('it', processors='tokenize,pos,lemma')
stanza_nl = stanza.Pipeline('nl', processors='tokenize,pos,lemma')
stanza_pt = stanza.Pipeline('pt', processors='tokenize,pos,lemma')
stanza_ar = stanza.Pipeline('ar', processors='tokenize,pos,lemma')
print("Stanza model initialization ends")

print("SpaCy model initialization starts")
spacy_en_sm = spacy.load("en_core_web_sm")
spacy_en_lg = spacy.load("en_core_web_lg")
spacy_zh = spacy.load("zh_core_web_sm")
spacy_es = spacy.load("es_core_news_sm")
spacy_ja = spacy.load("ja_core_news_sm")
spacy_de = spacy.load("de_core_news_sm")
spacy_fr = spacy.load("fr_core_news_sm")
spacy_it = spacy.load("it_core_news_sm")
spacy_nl = spacy.load("nl_core_news_sm")
spacy_pt = spacy.load("pt_core_news_sm")
print("SpaCy model initialization ends")

print("UDpipe model initialization starts")
udpipe_en = spacy_udpipe.load("en")
udpipe_zh = spacy_udpipe.load("zh")
udpipe_es = spacy_udpipe.load("es")
udpipe_ja = spacy_udpipe.load("ja")
udpipe_de = spacy_udpipe.load("de")
udpipe_fr = spacy_udpipe.load("fr")
udpipe_it = spacy_udpipe.load("it")
udpipe_nl = spacy_udpipe.load("nl")
udpipe_pt = spacy_udpipe.load("pt")
udpipe_ar = spacy_udpipe.load("ar")
print("UDpipe model initialization ends")

model_lang_map["spacy"] = {"eng_sm": spacy_en_sm, "eng_lg":spacy_en_lg, "cmn": spacy_zh, "spa": spacy_es, "fre": spacy_fr, "ger": spacy_de, "jpn": spacy_ja, "ita" : spacy_it, "dut": spacy_nl, "prt": spacy_pt }
model_lang_map["stanza"] = {"eng": stanza_en, "cmn": stanza_zh, "spa": stanza_es, "fre": stanza_fr, "ger": stanza_de, "jpn": stanza_ja, "ita" : stanza_it, "dut": stanza_nl, "prt": stanza_pt, "ara": stanza_ar }
model_lang_map["udpipe"] = {"eng": udpipe_en, "cmn": udpipe_zh, "spa": udpipe_es, "fre": udpipe_fr, "ger": udpipe_de, "jpn": udpipe_ja, "ita" : udpipe_it, "dut": udpipe_nl , "prt": udpipe_pt, "ara": udpipe_ar }

################################ Processor Functions ################################
# Define the functions to read outputs from STANZA
def get_services_stanza(docs):
    index = -1
    sentIndex = 0
    tokens = [] # score token objects
    nlpTokenList = [] # score token text
    nlpWordsList = []
    nlpPOSList = []
    nlpLemmaList = []
    nlpSentenceEndPositions = []
    hasCompoundWords = False

    for sentence in docs.sentences:
        sentIndex+=len(sentence.tokens)
        nlpSentenceEndPositions.append(sentIndex)
        for token in sentence.tokens:
            index += 1
            nlpTokenList.append(token.text)
            if len(token.words) == 1:
                # 1 word per token
                nlpWordsList.append(None)
                nlpPOSList.append(token.words[0].pos)
                nlpLemmaList.append(token.words[0].lemma)
            else:
                # N words per token
                hasCompoundWords = True
                tokenWords = []
                tokenLemmas = []
                tokenPOStags = []
                for word in token.words:
                    tokenWords.append(word.text)
                    tokenLemmas.append(word.lemma)
                    tokenPOStags.append(word.pos)
                nlpWordsList.append(tokenWords)
                nlpPOSList.append(tokenPOStags)
                nlpLemmaList.append(tokenLemmas)

    return nlpTokenList, nlpSentenceEndPositions, nlpLemmaList, nlpPOSList, nlpWordsList, hasCompoundWords

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
        nlpNerList.append([token.ent_iob_, token.ent_type_])

    return nlpTokenList, nlpSentenceEndPositions, nlpLemmaList, nlpPOSList


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

def get_tokens_per_sents(end_pos):
    res = []
    start = 0
    for end in end_pos:
        res.append(end - start)
        start = end
    return res

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
    packages = data['packages']

    final_HTML = ""
    header_HTML = "<div class='title'>"
    if "stanza" in packages:
        # Initialize the TexAS document
        mydoc = tx.Document(string)
        mydoc.meta().set("authors","hegler,yiwen,celine,yuqian")
        mydoc.date().setTimestamp("2021-01-19T14:44")

        model = model_lang_map["stanza"][lang]
        docs = model(string)
        tokens, end_pos, lemma, pos, nlpWordsList, hasCompoundWords = get_services_stanza(docs)

        mydoc.setTokenList(tokens, indexed=True)
        mydoc.views().get("TOKENS").meta().set("generator", "stanza")
        mydoc.views().get("TOKENS").meta().set("model", "stanza" + "-" + lang )
        mydoc.setSentenceList(end_pos)

        if hasCompoundWords:
            mydoc.addTokenView( "WORDS", nlpWordsList )
        mydoc.addTokenView("LEMMA", lemma)
        mydoc.addTokenView("POS", pos)
        
        # Extract HTML View
        myTabView = tx.UITabularView(mydoc)
        if hasCompoundWords:
            myTabView.showView("WORDS")
        myTabView.showView("LEMMA", labelCSS=False)
        myTabView.showView("POS")

        # concatenate the myTabView.HTML()
        header_HTML += "Stanza-" + lang + ": " + str(len(end_pos)) + " sentences; " + str(len(tokens)) + " tokens " + str(get_tokens_per_sents(end_pos)) + "<br>"
        final_HTML += "<div class='subtitle'>Stanza-" + lang + "</div> <br>" + myTabView.HTML().replace("\n", "") + '<br>'

    if "spacy" in packages:
        # Initialize the TexAS document
        if lang != 'eng':
            mydoc = tx.Document(string)
            mydoc.meta().set("authors","hegler,yiwen,celine,yuqian")
            mydoc.date().setTimestamp("2021-01-19T14:44")

            model = model_lang_map["spacy"][lang]
            docs = model(string)
            tokens, end_pos, lemma, pos = get_services_spacy(docs)

            mydoc.setTokenList(tokens, indexed=True)
            mydoc.views().get("TOKENS").meta().set("generator", "spacy")
            mydoc.views().get("TOKENS").meta().set("model", "spacy" + "-" + lang )
            mydoc.setSentenceList(end_pos)
            mydoc.addTokenView("LEMMA", lemma)
            mydoc.addTokenView("POS", pos)
        
            # Extract HTML View
            myTabView = tx.UITabularView(mydoc)
            myTabView.showView("LEMMA", labelCSS=False)
            myTabView.showView("POS")

            # concatenate the myTabView.HTML()
            header_HTML += "SpaCy-" + lang + " " + model.meta['name'] + ": " + str(len(end_pos)) + " sentences; " + str(len(tokens)) + " tokens " + str(get_tokens_per_sents(end_pos)) + "<br>"
            final_HTML += "<div class='subtitle'>" + "SpaCy-" + lang + " " + model.meta['name'] + "</div><br>" + myTabView.HTML().replace("\n", "") + '<br>'
        else:
            for langx in ("eng_sm", "eng_lg"):
                mydoc = tx.Document(string)
                mydoc.meta().set("authors","hegler,yiwen,celine,yuqian")
                mydoc.date().setTimestamp("2021-01-19T14:44")

                model = model_lang_map["spacy"][langx]
                docs = model(string)
                tokens, end_pos, lemma, pos = get_services_spacy(docs)

                mydoc.setTokenList(tokens, indexed=True)
                mydoc.views().get("TOKENS").meta().set("generator", "spacy")
                mydoc.views().get("TOKENS").meta().set("model", "spacy" + "-" + langx )
                mydoc.setSentenceList(end_pos)
                mydoc.addTokenView("LEMMA", lemma)
                mydoc.addTokenView("POS", pos)
            
                # Extract HTML View
                myTabView = tx.UITabularView(mydoc)
                myTabView.showView("LEMMA", labelCSS=False)
                myTabView.showView("POS")

                # concatenate the myTabView.HTML()
                header_HTML += "SpaCy-" + lang + " " + model.meta['name'] + ": " + str(len(end_pos)) + " sentences; " + str(len(tokens)) + " tokens " + str(get_tokens_per_sents(end_pos)) + "<br>"
                final_HTML += "<div class='subtitle'>" + "SpaCy-" + lang + " " + model.meta['name'] + "</div><br>" + myTabView.HTML().replace("\n", "") + '<br>'

    if "udpipe" in packages:
        model = model_lang_map["udpipe"][lang]
        docs = model(string)
        tokens, end_pos, lemma, pos = get_services_udpipe(docs)
        string = " ".join(tokens)

        # Initialize the TexAS document
        mydoc = tx.Document(string)
        mydoc.meta().set("authors","hegler,yiwen,celine,yuqian")
        mydoc.date().setTimestamp("2021-01-19T14:44")

        mydoc.setTokenList(tokens, indexed=True)
        mydoc.views().get("TOKENS").meta().set("generator", "udpipe")
        mydoc.views().get("TOKENS").meta().set("model", "udpipe" + "-" + lang )
        mydoc.setSentenceList(end_pos)
        mydoc.addTokenView("LEMMA", lemma)
        mydoc.addTokenView("POS", pos)
        
        # Extract HTML View
        myTabView = tx.UITabularView(mydoc)
        myTabView.showView("LEMMA", labelCSS=False)
        myTabView.showView("POS")

        # concatenate the myTabView.HTML()
        header_HTML += "UDpipe-" + lang + ": " + str(len(end_pos)) + " sentences; " + str(len(tokens)) + " tokens " + str(get_tokens_per_sents(end_pos)) + "<br>"
        final_HTML += "<div class='subtitle'>UDpipe-" + lang + "</div> <br>" + myTabView.HTML().replace("\n", "")

    header_HTML += "</div>"
    return header_HTML + "<br><br>" + final_HTML

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
