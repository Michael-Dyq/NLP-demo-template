# Backend Design

Run basic spacy and integrate service in Wikifier.

What you need to provide?

e.g. input/output -> JSON
e.g. input: text -> output: JSON


https://github.com/jinruiyang/zeroshotdemo


-Spacy:
python -m spacy download en_core_web_sm
import spacy
model = spacy.load("en_core_web_sm")
r = model(text)

-AllenNLP
from allennlp.predictors.predictor import Predictor
NER2018 = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/ner-model-2018.12.18.tar.gz")
SRL2019 = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/bert-base-srl-2019.06.17.tar.gz")

r2 = SRL2019.predict(text)

#json input vs url parameter
process json input first -> process url parameter
