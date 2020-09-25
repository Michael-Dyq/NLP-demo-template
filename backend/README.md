# Backend Design

We will use the PoS Tagging service of Spacy as an example


# How to Run it

Run "!python backend_cherry.py" and visit http://localhost:8081. You may change the port number.

# How to Curl the Data

## For Windows

### JSON input:
curl.exe -H "Content-Type: application/json" -X POST http://localhost:8081/json -d "{"text":"I love cat"}"

### String input:
curl.exe -d 'text=I+like+sushi' http://localhost:8081/anns

# How to Make your Own Demo
## Step 1: Load the Model

for Spacy we have the following:
!python -m spacy download en_core_web_sm

import spacy
model = spacy.load("en_core_web_sm")
r = model(text)

## Step 2: Figure out the format of Input (String v.s. JSON)

If you would like your service to take both kinds of inputs. You should design two separate paths for string and json

## Step 3: Return the output as a JSON document

Once we finish annotating the text, we want to load the output in a JSON document and return it


# Reference:

-CherryPy Backend Example

https://github.com/jinruiyang/zeroshotdemo

-AllenNLP (Not Supported on Window)

from allennlp.predictors.predictor import Predictor
SRL2019 = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/bert-base-srl-2019.06.17.tar.gz")

r2 = SRL2019.predict(text)