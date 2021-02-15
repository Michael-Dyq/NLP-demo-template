'''
Current version
+---------------------------------------+
+ spacy == 3.0.1                        +
+ en-core-web-lg == 3.0.0               +
+ zh-core-web-lg == 3.0.0               +
+ es_core_news_lg == 3.0.0              +
+---------------------------------------+
'''


import json
import texas as tx
import spacy

# create a document

TXLang = "en"
TXText = "Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis, a clinical method for treating psychopathology through dialogue between a patient and a psychoanalyst. Freud was born to Galician Jewish parents in the Moravian town of Freiberg, in the Austrian Empire."

TXSpacyModel = TXLang

nlp_en = spacy.load("en_core_web_sm")
#nlp_en = spacy.load("en_core_web_lg")

print ("Processing text: ",TXText)

doc = nlp_en(TXText)

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
myTabView.showView("NER")
myTabView.showView("CUSTOM")
print(myTabView.HTML())
print("------------")

print("")
print("end!")
print("")


#----------------------------------------------
#Chinese
TXLang = "zh"
TXText= "西格蒙德·弗洛伊德（Sigmund Freud）是奧地利的神經病學家，也是精神分析的創始人。精神分析是一種通過患者與精神分析人員之間的對話來治療精神病理的臨床方法。弗洛伊德出生於奧地利帝國摩拉維亞小鎮弗賴貝格的加利西亞猶太父母。他於1881年在維也納大學獲得醫學博士學位。弗洛伊德在維也納生活和工作，1886年在維也納開始了臨床工作。1938年，弗洛伊德離開奧地利，逃避了納粹的迫害。 他於1939年在英國流亡。"

TXSpacyModel = TXLang

nlp_zh = spacy.load("zh_core_web_sm")
#nlp_zh = spacy.load("zh_core_web_lg")

print ("Processing text: ",TXText)

doc = nlp_zh(TXText)

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
[['PERSON', 0], ['PERSON', 2], ['GPE', 6], ['PERSON', 41], ['GPE', 43], ['PERSON', 48], ['PERSON', 49], ['ORG', 51], ['GPE', 52], ['DATE', 59], ['PERSON', 70], ['DATE', 79], ['DATE', 89], ['PERSON', 91], ['DATE', 102], ['GPE', 104]]
'''
mydoc1.addTokenView( "POS", nlpPOSList )
# no "DEP" annotations resulting from stanza
# mydoc1.addTokenView( "POS-DEP", nlpDEPList )
mydoc1.addTokenView( "LEMMA", nlpLemmaList )
mydoc1.addSpanView( "NER", nerList )
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
myTabView.showView("NER")
myTabView.showView("CUSTOM")
print(myTabView.HTML())
print("------------")

print("")
print("end!")
print("")


#----------------------------------------------------------
#Spanish
TXLang = "es"
TXText= "Sigmund Freud fue un neurólogo austriaco y fundador del psicoanálisis, un método clínico para tratar la psicopatología a través del diálogo entre un paciente y un psicoanalista. Freud nació de padres judíos gallegos en la ciudad morava de Freiberg, en el Imperio austríaco. Se graduó como doctor en medicina en 1881 en la Universidad de Viena. Freud vivió y trabajó en Viena, donde estableció su práctica clínica en 1886. En 1938, Freud dejó Austria para escapar de la persecución nazi. Murió exiliado en el Reino Unido en 1939."

TXSpacyModel = TXLang

nlp_es = spacy.load("es_core_news_sm")
#nlp_es = spacy.load("es_core_news_lg")

print ("Processing text: ",TXText)

doc = nlp_es(TXText)

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
[['PER', 0, 2], ['PER', 29], ['LOC', 40], ['LOC', 44, 46], ['ORG', 57, 60], ['PER', 61], ['LOC', 66], ['PER', 79], ['LOC', 81], ['MISC', 89, 95]]'''
mydoc1.addTokenView( "POS", nlpPOSList )
# no "DEP" annotations resulting from stanza
# mydoc1.addTokenView( "POS-DEP", nlpDEPList )
mydoc1.addTokenView( "LEMMA", nlpLemmaList )
mydoc1.addSpanView( "NER", nerList )
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
myTabView.showView("NER")
myTabView.showView("CUSTOM")
print(myTabView.HTML())
print("------------")

print("")
print("end!")
print("")

