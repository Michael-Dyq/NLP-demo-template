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