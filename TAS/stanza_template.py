import stanza

# download English model
# stanza.download('en')

# initialize English neural pipeline
nlp = stanza.Pipeline('en')

'''
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
doc = nlp("Barack Obama was born in Hawaii. He loves sushi.") 

# print(doc)
# print(doc.entities)