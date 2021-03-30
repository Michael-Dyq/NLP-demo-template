import os.path
import time
from datetime import datetime
import json
import csv
from collections import defaultdict
from typing import DefaultDict, Text
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
stanza_ru = stanza.Pipeline('ru', processors='tokenize,pos,lemma')
print("Stanza model initialization ends")

print("SpaCy model initialization starts")
spacy_en = spacy.load("en_core_web_sm")
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
udpipe_ru = spacy_udpipe.load("ru")
print("UDpipe model initialization ends")


model_lang_map["spacy"] = {"eng": spacy_en, "cmn": spacy_zh, "spa": spacy_es, "fre": spacy_fr, "ger": spacy_de, "jpn": spacy_ja, "ita" : spacy_it, "dut": spacy_nl, "prt": spacy_pt }
model_lang_map["stanza"] = {"eng": stanza_en, "cmn": stanza_zh, "spa": stanza_es, "fre": stanza_fr, "ger": stanza_de, "jpn": stanza_ja, "ita" : stanza_it, "dut": stanza_nl, "prt": stanza_pt, "ara": stanza_ar, "rus": stanza_ru }
model_lang_map["udpipe"] = {"eng": udpipe_en, "cmn": udpipe_zh, "spa": udpipe_es, "fre": udpipe_fr, "ger": udpipe_de, "jpn": udpipe_ja, "ita" : udpipe_it, "dut": udpipe_nl , "prt": udpipe_pt, "ara": udpipe_ar, "rus": udpipe_ru }

################################ Cache Loading ################################
with open('/cache/cache_stanza.json') as file_obj:
    cache_stanza = json.load(file_obj)


with open('/cache/cache_spacy.json') as file_obj:
    cache_spacy = json.load(file_obj)


with open('/cache/cache_udpipe.json') as file_obj:
    cache_udpipe = json.load(file_obj)


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


def get_header_table(summary_list):
    table_HTML = '<table class=\"summary\" cellspacing=\"10\">'
    table_HTML += "<tr>"
    table_HTML += "<th class=\'w3-center\'>package</th>"
    table_HTML += "<th class=\'w3-center\'>#sentences</th>"
    table_HTML += "<th class=\'w3-center\'>#tokens</th>"
    table_HTML += "<th class=\'w3-center\'>#tokens/sentence</th>"
    table_HTML += "</tr>"


    for model_name, num_sents, num_tokens, tokens_per_sent in summary_list:
        table_HTML += "<tr>"
        table_HTML += "<td class=\'w3-center\'>" + model_name
        table_HTML += "<td class=\'w3-center\'>" + num_sents
        table_HTML += "<td class=\'w3-center\'>" + num_tokens
        table_HTML += "<td class=\'w3-center\'>" + tokens_per_sent
        table_HTML += "</tr>"

    table_HTML += "</table>"

    return table_HTML


def writeLog(row):
    # Initialize the log.csv
    with open('log.csv','a') as f:
        writer=csv.writer(f)
        writer.writerow(row)


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
    message_HTML = "<div class=\'message\'>"
    isMessage = False
    header_input = []
    log_row = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), lang]

    if "stanza" in packages:
        # Initialize the TexAS document
        mydoc = tx.Document(string)
        mydoc.meta().set("authors","hegler,yiwen,celine,yuqian")
        mydoc.date().setTimestamp("2021-01-19T14:44")

        ## Check text whether is already in cache
        if string in cache_stanza[lang].keys():
            tokens = cache_stanza[lang][string]['tokens']
            end_pos = cache_stanza[lang][string]['end_pos']
            lemma = cache_stanza[lang][string]['lemma']
            pos = cache_stanza[lang][string]['pos']
            nlpWordsList = cache_stanza[lang][string]['nlpWordsList']
            hasCompoundWords = cache_stanza[lang][string]['hasCompoundWords']
            print("--------------This information is loaded from cache_stanza--------------")
        else:
            model = model_lang_map["stanza"][lang]
            docs = model(string)
            tokens, end_pos, lemma, pos, nlpWordsList, hasCompoundWords = get_services_stanza(docs)
            cache_stanza[lang][string] = {}
            cache_stanza[lang][string]['tokens'] = tokens
            cache_stanza[lang][string]['end_pos'] = end_pos
            cache_stanza[lang][string]['lemma'] = lemma
            cache_stanza[lang][string]['pos'] = pos
            cache_stanza[lang][string]['nlpWordsList'] = nlpWordsList
            cache_stanza[lang][string]['hasCompoundWords'] = hasCompoundWords
            print("--------------This information is not include in cache_stanza--------------")
            
        mydoc.setTokenList(tokens, indexed=True)
        mydoc.views().get("TOKENS").meta().set("generator", "stanza")
        mydoc.views().get("TOKENS").meta().set("model", "stanza" + "-" + lang)
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
        header_input.append(("Stanza", str(len(end_pos)) , str(len(tokens)), str(get_tokens_per_sents(end_pos))))
        final_HTML += "<div class='subtitle'>Stanza</div> <br>" + myTabView.HTML().replace("\n", "") + "<br>"
        log_row.append("stanza")
    
    else:
        log_row.append("")

    if "spacy" in packages:
        # SpaCy does not support Arabic and Russian
        if lang == 'ara' or lang == 'rus':
            message_HTML += "SpaCy does not support Arabic or Russian. <br>"
            isMessage = True

        else:
            mydoc = tx.Document(string)
            mydoc.meta().set("authors","hegler,yiwen,celine,yuqian")
            mydoc.date().setTimestamp("2021-01-19T14:44")

            ## Check text whether is already in cache
            if string in cache_spacy[lang].keys():
                tokens = cache_spacy[lang][string]['tokens']
                end_pos = cache_spacy[lang][string]['end_pos']
                lemma = cache_spacy[lang][string]['lemma']
                pos = cache_spacy[lang][string]['pos']
                print("--------------This information is loaded from cache_spacy--------------")
            else:
                model = model_lang_map["spacy"][lang]
                docs = model(string)
                tokens, end_pos, lemma, pos = get_services_spacy(docs)
                cache_spacy[lang][string] = {}
                cache_spacy[lang][string]['tokens'] = tokens
                cache_spacy[lang][string]['end_pos'] = end_pos
                cache_spacy[lang][string]['lemma'] = lemma
                cache_spacy[lang][string]['pos'] = pos
                print("--------------This information is not included in cache_spacy--------------")

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
            header_input.append(("SpaCy", str(len(end_pos)) , str(len(tokens)), str(get_tokens_per_sents(end_pos))))
            final_HTML += "<div class='subtitle'>" + "SpaCy" + "</div><br>" + myTabView.HTML().replace("\n", "") + "<br>"
        log_row.append("spacy")
    
    else:
        log_row.append("")

    if "udpipe" in packages:
        ## Check text whether is already in cache
        if string in cache_udpipe[lang].keys():
            tokens = cache_udpipe[lang][string]['tokens']
            end_pos = cache_udpipe[lang][string]['end_pos']
            lemma = cache_udpipe[lang][string]['lemma']
            pos = cache_udpipe[lang][string]['pos']
            print("--------------This information is loaded from cache_udpipe--------------")
        else:
            model = model_lang_map["udpipe"][lang]
            docs = model(string)
            tokens, end_pos, lemma, pos = get_services_udpipe(docs)
            cache_udpipe[lang][string] = {}
            cache_udpipe[lang][string]['tokens'] = tokens
            cache_udpipe[lang][string]['end_pos'] = end_pos
            cache_udpipe[lang][string]['lemma'] = lemma
            cache_udpipe[lang][string]['pos'] = pos
            
            print("--------------This information is not included in cache_udpipe--------------")

        #string = " ".join(tokens)

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
        header_input.append(("UDpipe", str(len(end_pos)) , str(len(tokens)), str(get_tokens_per_sents(end_pos))))
        final_HTML += "<div class='subtitle'>UDpipe</div> <br>" + myTabView.HTML().replace("\n", "") + "<br>"
        log_row.append("udpipe")
    
    else:
        log_row.append("")

    message_HTML += "</div>"
    if isMessage:
        return message_HTML + get_header_table(header_input) + "<br><br>" + final_HTML

    writeLog(log_row)
    return get_header_table(header_input) + "<br><br>" + final_HTML


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
