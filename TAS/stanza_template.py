import stanza

# download English, Chinese, and Spanish model (takes a while)
# stanza.download('en')
# stanza.download('zh')
# stanza.download('es')

print("Initialization starts")

# initialize English neural pipeline
nlp_en = stanza.Pipeline('en')

# initialize English neural pipeline
nlp_zh = stanza.Pipeline('zh')

# initialize English neural pipeline
nlp_es = stanza.Pipeline('es')

if not nlp_en: # or not nlp_es or not nlp_zh:
    print("Initialization fails!")

'''
Optional:

# OPTION 1: specify processor
stanza.download('zh', processors='tokenize, pos')
nlp = stanza.Pipeline('zh', processors='tokenize, pos')

# OPTION 2: specify processors and package
stanza.download('nl', processors={'ner': 'wikiner'}, package='lassysmall')
nlp = stanza.Pipeline('nl', processors={'ner': 'wikiner'}, package='lassysmall')

# Complex Example
processor_dict = {
    'tokenize': 'gsd', 
    'pos': 'hdt', 
    'ner': 'conll03', 
    'lemma': 'default'
}
stanza.download('de', processors=processor_dict, package=None)
nlp = stanza.Pipeline('de', processors=processor_dict, package=None)
'''

# run annotation over a sentence
doc_en = nlp_en("I like sushi. He likes fish. She likes steak.") 
doc_es = nlp_es("Barack Obama nació en Hawaii. Le encanta el sushi.")
doc_zh = nlp_zh("巴拉克·奥巴马在夏威夷出生。他喜欢寿司。")



print("Chinese Tokens and Sentences")
print([sentence.text for sentence in doc_zh.sentences])
print([token.text for sentence in doc_zh.sentences for token in sentence.tokens])
end_pos = []
id = 0
for sentence in doc_zh.sentences:
    id += len(sentence.tokens)
    end_pos.append(id)
    
print(end_pos)


print("English Tokens and Sentences")
print([token.text for sentence in doc_en.sentences for token in sentence.tokens])
end_pos = []
id = 0
for sentence in doc_en.sentences:
    id += len(sentence.tokens)
    end_pos.append(id)

print(end_pos)

print("Spanish Tokens and Sentences")
print([sentence.text for sentence in doc_es.sentences])
print([token.text for sentence in doc_es.sentences for token in sentence.tokens])
end_pos = []
id = 0
for sentence in doc_es.sentences:
    id += len(sentence.tokens)
    end_pos.append(id)
    
print(end_pos)