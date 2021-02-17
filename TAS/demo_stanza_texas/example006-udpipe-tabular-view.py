'''
spacy-udpipe 0.3.2 has requirement spacy<3.0.0,>=2.1.0,
+--------------------------+
+ spacy 2.3.5              +
+                          +
+--------------------------+
'''

#pip install spacy-udpipe


import json
import texas as tx
import spacy_udpipe
print('-------------pass----------')
#spacy_udpipe.download("en")

# create a document

TXLang = "en"
TXText = "Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis, a clinical method for treating psychopathology through dialogue between a patient and a psychoanalyst. Freud was born to Galician Jewish parents in the Moravian town of Freiberg, in the Austrian Empire."

TXSpacyModel = TXLang

nlp_en = spacy_udpipe.load(TXLang)

doc = nlp_en(TXText)

index = -1#should we rename this variable in order to spacify what index it stands for?
sentIndex = 0
nlpTokenList = []
nlpPOSList = []
nlpDEPList = []
nlpLemmaList = []
#nlpNerList = [] #new add
nlpSentenceEndPositions = []

for sentence in doc.sents:
    sentIndex+=len(sentence)
    nlpSentenceEndPositions.append(sentIndex)


for token in doc: 
    index += 1
    nlpTokenList.append(token.text)
    nlpPOSList.append(token.pos_)
    nlpLemmaList.append(token.lemma_)
    #nlpNerList.append([token.ent_iob_, token.ent_type_]) # eg:[['B','NORP'],['O',''],...]


    mydoc1 = tx.Document(TXText, TXLang)
# mydoc1.meta().set("generator","stanza")
# mydoc1.meta().set("model",TXSpacyModel)

mydoc1.setTokenList(nlpTokenList, indexed=True)
mydoc1.views().get("TOKENS").meta().set("generator","spacy")
mydoc1.views().get("TOKENS").meta().set("model",TXSpacyModel)
mydoc1.setSentenceList( nlpSentenceEndPositions )


'''
NER
'''


mydoc1.addTokenView( "POS", nlpPOSList )
# no "DEP" annotations resulting from stanza
# mydoc1.addTokenView( "POS-DEP", nlpDEPList )
mydoc1.addTokenView( "LEMMA", nlpLemmaList )
#mydoc1.addSpanView( "NER", nerList )
mydoc1.addSpanView( "CUSTOM", [ {"label":"PHRASAL-VERB", "start_token":28, "final_token":30} ] )

# create another document reversing from the previous document JSON 
mydoc2 = tx.reverse(mydoc1.TAS())

print("==========")
print("mydoc2")
print("----------")
print( "--- Document TAS" )
print( json.dumps(mydoc2.TAS()) )
print( "--- Token List" )
print( mydoc2.getTokenList() )
print( "--- Token Info" )
print( json.dumps( mydoc2.getTokenInfo() ) )
print( "--- Sentence Info" )
print( json.dumps( mydoc2.getSentenceInfo() ) )

print("")
print("============")
print("Tabular View")
print("------------")
myTabView = tx.UITabularView(mydoc2)
myTabView.showView("POS")
myTabView.showView("LEMMA", labelCSS=False)
#myTabView.showView("NER")
myTabView.showView("CUSTOM")
print(myTabView.HTML())
print("------------")

print("")
print("end!")
print("")






    
