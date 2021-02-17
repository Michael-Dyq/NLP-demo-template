import sys
import os
import argparse
import datetime
import spacy_udpipe


# download language models

# spacy_udpipe.download("en")
# spacy_udpipe.download("zh")
# spacy_udpipe.download("es")

nlp_en = spacy_udpipe.load("en")
nlp_zh = spacy_udpipe.load("zh")
nlp_es = spacy_udpipe.load("es")

text_en = "I like sushi. He likes fish. She likes steak."
text_es = "Barack Obama nació en Hawaii. Le encanta el sushi."
text_zh = "巴拉克·奥巴马在夏威夷出生。他喜欢寿司"

# English Model
doc = nlp_en(text_en)

tokens = []
for token in doc:
    tokens.append(token.text)

print(tokens)

end_pos = []
for sent in doc.sents:
    end_pos.append(sent.end)

print(end_pos)


# Chinese Model
doc = nlp_zh(text_zh)

tokens = []
for token in doc:
    tokens.append(token.text)

print(tokens)

end_pos = []
for sent in doc.sents:
    end_pos.append(sent.end)

print(end_pos)

# Spanish Model
doc = nlp_es(text_es)

tokens = []
for token in doc:
    tokens.append(token)

print(tokens)

end_pos = []
for sent in doc.sents:
    end_pos.append(sent.end)

print(end_pos)