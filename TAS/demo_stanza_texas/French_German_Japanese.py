import json
import texas as tx
import spacy

# create a document
'''
TXLang = "fr"
TXText = "Apple cherche à acheter une start-up anglaise pour 1 milliard de dollars."
nlp = spacy.load("fr_core_news_sm")

TXLang = "de"
TXText = "Sigmund Freud war ein österreichischer Neurologe und der Begründer der Psychoanalyse, einer klinischen Methode zur Behandlung der Psychopathologie im Dialog zwischen einem Patienten und einem Psychoanalytiker. Freud wurde als Sohn galizischer jüdischer Eltern im mährischen Freiberg im österreichischen Reich geboren. Er qualifizierte sich 1881 als Doktor der Medizin an der Universität Wien. Freud lebte und arbeitete in Wien, nachdem er dort 1886 seine klinische Praxis eingerichtet hatte. 1938 verließ Freud Österreich, um der nationalsozialistischen Verfolgung zu entgehen. Er starb 1939 im britischen Exil."
nlp = spacy.load("de_core_news_sm")
'''

TXLang = "ja"
TXText = "アップルがイギリスの新興企業を１０億ドルで購入を検討"

nlp = spacy.load("ja_core_news_sm")

TXSpacyModel = TXLang


print ("Processing text: ",TXText)

doc = nlp(TXText)

index = -1
  #should we rename this variable in order to spacify what index it stands for?
sentIndex = 0
nlpTokenList = []
nlpPOSList = []
nlpDEPList = []
nlpLemmaList = []
nlpNerList = [] #new add
nlpSentenceEndPositions = []

for sentence in doc.sents:
    sentIndex+=len(sentence)
    nlpSentenceEndPositions.append(sentIndex)

for token in doc:
    #w = word
    # what is this for？
    # print(word.text, word.pos, word.lemma) # , word.ner) 
    index += 1
    nlpTokenList.append(token.text)
    nlpPOSList.append(token.pos_)
    nlpLemmaList.append(token.lemma_)
    nlpNerList.append([token.ent_iob_, token.ent_type_]) # eg:[['B','NORP'],['O',''],...]
    

    
mydoc1 = tx.Document(TXText, TXLang)
# mydoc1.meta().set("generator","stanza")
# mydoc1.meta().set("model",TXSpacyModel)

mydoc1.setTokenList(nlpTokenList, indexed=True)
mydoc1.views().get("TOKENS").meta().set("generator","spacy")
mydoc1.views().get("TOKENS").meta().set("model",TXSpacyModel)
mydoc1.setSentenceList( nlpSentenceEndPositions )

# NER

nerList = []


word_index = 0
 #Does word_index represent the index of token?
start_token, inside_token, final_token = -1,-1,-1
contin = True  # This variable helps to record the start_index of the first entity.
for idx in range(len(nlpNerList)):
    token_iob, token_ner = nlpNerList[idx]
    if token_iob == 'B':
        # Just record the start_index of the first entity and do not update the nerList
        if len(nerList) == 0 and contin:
            start_token = word_index
            nerLabelStart = token_ner
            contin=False
            
        # Update the information of NE into the nerList        
        else:

            if start_token < final_token:
                nerList.append([nerLabelStart, start_token, final_token+1])
            else:
                nerList.append([nerLabelStart, start_token])
            # Record the new start_index for the next entity
            start_token = word_index
            nerLabelStart = token_ner
            
    if token_iob == 'I':
        inside_token = word_index


    if token_iob == 'O':
        final_token = inside_token
            
    word_index += 1
    
# Finally, add the last ner into the nerList
if start_token == -1:
    pass
else:
    if start_token < final_token:
       nerList.append([nerLabelStart, start_token, final_token+1])
    else:
       nerList.append([nerLabelStart, start_token])

print(nerList)
'''
[['PERSON', 0], ['PERSON', 0, 2], ['NORP', 4], ['PERSON', 27], ['NORP', 31], ['NORP', 32],
['NORP', 36], ['GPE', 39], ['GPE', 42, 45]]
'''

mydoc1.addTokenView( "POS", nlpPOSList )
# no "DEP" annotations resulting from stanza
# mydoc1.addTokenView( "POS-DEP", nlpDEPList )
mydoc1.addTokenView( "LEMMA", nlpLemmaList )
mydoc1.addSpanView( "NER", nerList )
#mydoc1.addSpanView( "CUSTOM", [ {"label":"PHRASAL-VERB", "start_token":28, "final_token":30} ] )

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
myTabView.showView("NER")
#myTabView.showView("CUSTOM")
print(myTabView.HTML())
print("------------")

print("")
print("end!")
print("")

