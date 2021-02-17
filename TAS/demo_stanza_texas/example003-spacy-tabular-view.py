import json
import texas as tx
import spacy

# create a document

TXLang = "en"
TXText = "Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis, a clinical method for treating psychopathology through dialogue between a patient and a psychoanalyst. Freud was born to Galician Jewish parents in the Moravian town of Freiberg, in the Austrian Empire."
TXSpacyModel = TXLang+"_core_web_sm"

nlp = spacy.load(TXSpacyModel)

doc = nlp(TXText)

print(doc.text)
index = -1
nlpTokenList = []
nlpPOSList = []
nlpDEPList = []
nlpLemmaList = []
nlpSentenceEndPositions = []

for token in doc:
    index += 1
    nlpTokenList.append(token.text)
    nlpPOSList.append(token.pos_)
    nlpDEPList.append(token.dep_)
    nlpLemmaList.append(token.lemma_)
    if token.is_sent_end:
        nlpSentenceEndPositions.append(index+1)

mydoc1 = tx.Document(TXText, TXLang)
# mydoc1.meta().set("generator","spacy")
# mydoc1.meta().set("model",TXSpacyModel)

mydoc1.setTokenList( nlpTokenList, indexed=True )
mydoc1.views().get("TOKENS").meta().set("generator","spacy")
mydoc1.views().get("TOKENS").meta().set("model",TXSpacyModel)

mydoc1.setSentenceList( nlpSentenceEndPositions )

mydoc1.addTokenView( "POS", nlpPOSList )
mydoc1.addTokenView( "POS-DEP", nlpDEPList )
mydoc1.addTokenView( "LEMMA", nlpLemmaList )

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
myTabView.showView("POS-DEP")
myTabView.showView("LEMMA",labelCSS=False)
print(myTabView.HTML())
print("------------")

print("")
print("end!")
print("")

