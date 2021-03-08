import json
import texas as tx
import stanza

# create a document

TXLang = "pt"
TXText = "Apple está querendo comprar uma startup do Reino Unido por 100 milhões de dólares."
# TXText = "Boa noite!"

TXSpacyModel = TXLang

nlp = stanza.Pipeline(TXSpacyModel,processors='tokenize,pos,lemma')

'''

IGNORE THIS PART, IT'S JUST AN EXAMPLE...

import stanza
nlp = stanza.Pipeline("pt",processors='tokenize,pos,lemma')
text = "Apple está querendo comprar uma startup do Reino Unido por 100 milhões de dólares. Boa noite!"
doc = nlp(text)

for sentence in doc.sentences:
    print(sentence.tokens)
s = doc.sentences[0]
    
for token in sentence.tokens:
    print(token)
t = s.tokens[7]

'''

print ("Processing text: ",TXText)

doc = nlp(TXText)

index = -1
sentIndex = 0
nlpTokenList = []
nlpWordsList = []
nlpPOSList = []
nlpDEPList = []
nlpLemmaList = []
nlpSentenceEndPositions = []
hasCompoundWords = False

for sentence in doc.sentences:
    sentIndex+=len(sentence.tokens)
    nlpSentenceEndPositions.append(sentIndex)
    for token in sentence.tokens:
        t = token
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
        
    #for word in sentence.words:
    #    w = word
    #    # print(word.text, word.pos, word.lemma) # , word.ner) 
    #    index += 1
    #    nlpTokenList.append(word.text)
    #    nlpPOSList.append(word.pos)
    #    nlpLemmaList.append(word.lemma)
        
print( "nlpTokenList" , len(nlpTokenList) , nlpTokenList)
print( "nlpWordsList" , len(nlpWordsList) , nlpWordsList )
print( "nlpPOSList" , len(nlpPOSList) , nlpPOSList )
print( "nlpLemmaList" , len(nlpLemmaList) , nlpLemmaList )

mydoc1 = tx.Document(TXText, TXLang)
# mydoc1.meta().set("generator","stanza")
# mydoc1.meta().set("model",TXSpacyModel)

mydoc1.setTokenList( nlpTokenList, indexed=True)
mydoc1.views().get("TOKENS").meta().set("generator","stanza")
mydoc1.views().get("TOKENS").meta().set("model",TXSpacyModel)
mydoc1.setSentenceList( nlpSentenceEndPositions )

if hasCompoundWords:
    mydoc1.addTokenView( "WORDS", nlpWordsList )
mydoc1.addTokenView( "LEMMA", nlpLemmaList )
mydoc1.addTokenView( "POS", nlpPOSList )

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
if hasCompoundWords:
    myTabView.showView("WORDS")
myTabView.showView("LEMMA", labelCSS=False)
myTabView.showView("POS")
print(myTabView.HTML())
print("------------")

print("")
print("end!")
print("")

