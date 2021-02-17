import stanza
import spacy_udpipe

# STANZA: download English, Chinese, and Spanish model (takes a while)
stanza.download('en')
stanza.download('zh')
stanza.download('es')

# UDPIPE: download English, Chinese, and Spanish model (takes a while)
spacy_udpipe.download("en")
spacy_udpipe.download("zh")
spacy_udpipe.download("es")

# SpaCy: run in command line
# python -m spacy download en_core_web_sm
# python -m spacy download zh_core_web_sm
# python -m spacy download es_core_news_sm

