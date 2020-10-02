# Backend Design

These scripts will demonstrate how to build a backend service with Python. We use the PoS Tagging service of Spacy and NER as an example.

## Setup the Environment

### Set up miniconda
curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
bash Miniconda-latest-Linux-x86_64.sh -p /shared/yiwent/miniconda -b
export  PATH=/shared/yiwent/miniconda/bin:${PATH}
conda update -y conda

### Add the Path to the Environment Variable
export  PATH=/shared/yiwent/miniconda/bin:${PATH}

### Install the Packages your Program Requires 
conda create -n ENV_NAME_HERE python=3.6
source activate ENV_NAME_HERE
pip install ...

In our case, we need to install the following packages and model:
pip install spacy
pip install cherrypy
python -m spacy download en_core_web_sm

## How to Run it
Run "python backend_cherry.py" in your terminal. The service is currently running on dickens:4033 and dickens:4034. You may alter the port number based on your need.

url_pos = 'http://dickens.seas.upenn.edu:4034/pos'
url_ner = 'http://dickens.seas.upenn.edu:4033/ner'

## How to Retrieve the Output

## Via Submitting Post Request on Python

Run python api_post_request_f.py

This script use an example string of 'Barack Obama is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017.', and calls two backend services mentioned above.

## Via Parameters:

We can also pass in the parameter directly in URL. In this case, we pass in a parameter called text, which is the string "I like sushi".

curl http://dickens.seas.upenn.edu:4034/pos?text=I+like+sushi

# How to Make your Own Demo
## Step 1: Load the Model

for Spacy we have the following:
!python -m spacy download en_core_web_sm

import spacy
model = spacy.load("en_core_web_sm")
r = model(text)

## Step 2: Figure out the format of Input (String v.s. JSON)

If you would like your service to take both kinds of inputs. You should implement the same path for both string and json. 

## Step 3: Return the output as a JSON document

Once we finish annotating the text, we want to load the output in a JSON document and return it


# Reference:

-CherryPy Backend Example

https://github.com/jinruiyang/zeroshotdemo

-AllenNLP (Not Supported on Window)

from allennlp.predictors.predictor import Predictor
SRL2019 = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/bert-base-srl-2019.06.17.tar.gz")

r2 = SRL2019.predict(text)
