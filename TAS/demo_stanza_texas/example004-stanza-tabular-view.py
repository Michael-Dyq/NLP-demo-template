import json
import texas as tx
import stanza

# create a document

TXLang = "en"
TXText = "Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis, a clinical method for treating psychopathology through dialogue between a patient and a psychoanalyst. Freud was born to Galician Jewish parents in the Moravian town of Freiberg, in the Austrian Empire."

TXSpacyModel = TXLang

nlp = stanza.Pipeline(TXSpacyModel,processors='tokenize,pos,lemma,ner')

print ("Processing text: ",TXText)

doc = nlp(TXText)

index = -1
sentIndex = 0
nlpTokenList = []
nlpPOSList = []
nlpDEPList = []
nlpLemmaList = []
nlpSentenceEndPositions = []

for sentence in doc.sentences:
    sentIndex+=len(sentence.tokens)
    nlpSentenceEndPositions.append(sentIndex)
    for word in sentence.words:
        w = word
        # print(word.text, word.pos, word.lemma) # , word.ner) 
        index += 1
        nlpTokenList.append(word.text)
        nlpPOSList.append(word.pos)
        nlpLemmaList.append(word.lemma)
        
mydoc1 = tx.Document(TXText, TXLang)
# mydoc1.meta().set("generator","stanza")
# mydoc1.meta().set("model",TXSpacyModel)

mydoc1.setTokenList( nlpTokenList, indexed=True)
mydoc1.views().get("TOKENS").meta().set("generator","stanza")
mydoc1.views().get("TOKENS").meta().set("model",TXSpacyModel)
mydoc1.setSentenceList( nlpSentenceEndPositions )

# NER

ner = []

tokens = [token for sentence in doc.sentences for token in sentence.tokens]
word_index = 0
for idx in range(len(tokens)):
    token = tokens[idx]
    if token.ner.startswith("S-"):
        nerLabel = token.ner[2:]
        # print(word_index, nerLabel)
        # ner.append( {"label":nerLabel, "start_token":word_index, "final_token":word_index+1} )
        # OR 
        ner.append( [nerLabel, word_index] )
    if token.ner.startswith("B-"):
        start_token = word_index
        nerLabelStart = token.ner[2:]
    if token.ner.startswith("E-"):
        final_token = word_index
        nerLabelFinal = token.ner[2:]
        if nerLabelStart == nerLabelFinal:
            # print(start_token, final_token, nerLabelFinal)
            # ner.append( {"label":nerLabelFinal, "start_token":start_token, "final_token":final_token+1} )
            # OR 
            ner.append( [nerLabelFinal, start_token, final_token+1] )
            nerLabelStart = ""
            nerLabelFinal = ""
    word_index += len(token.words)

print(ner)

mydoc1.addTokenView( "POS", nlpPOSList )
# no "DEP" annotations resulting from stanza
# mydoc1.addTokenView( "POS-DEP", nlpDEPList )
mydoc1.addTokenView( "LEMMA", nlpLemmaList )
mydoc1.addSpanView( "NER", ner )
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
#myTabView.showView("TOKENS")
#myTabView.showView("POS")
# myTabView.showView("LEMMA", labelCSS=False)
# myTabView.showView("NER")
# myTabView.showView("CUSTOM")
print(myTabView.HTML())
print("------------")

print("")
print("end!")
print("")

