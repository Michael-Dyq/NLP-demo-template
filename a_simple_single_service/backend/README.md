# Backend Design

These scripts will demonstrate how to build a simple single backend service with Python. We use the Tokenizer, PoS Tagging services of Spacy as an example.

## Setup the Environment

### Set up Miniconda

```linux
curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
bash Miniconda-latest-Linux-x86_64.sh -p /shared/{your-folder-name}/miniconda -b
export  PATH=/shared/yiwent/miniconda/bin:${PATH}
conda update -y conda
```

### Add the Path to the Environment Variable
```linux
export  PATH=/shared/{your-folder-name}/miniconda/bin:${PATH}
```

### Install the Packages your Program Requires

Please use the following commands to activate the conda environment install the required packages.

```linux
conda create -n ENV_NAME_HERE python=3.6
source activate ENV_NAME_HERE
pip install PACKAGE_NAME_HERE
```

Please download and install your model to the folder.
In our template, we need to install the following packages and model powered byt SpaCy.

```linux
pip install spacy
pip install cherrypy
python -m spacy download en_core_web_sm
```

## How to Run it
Run the command in your terminal. The service is currently running on http://localhost:8081. You may alter the port number based on your need.

 ```python
 python service_backend.py
 ```

url = 'http://localhost:8081/

## How to Retrieve the Output

## Via Submitting Post Request on Python

This script use an example string of 'Barack Obama is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017.', and calls two backend services mentioned above. You need to modify the port number and urls based on where your service is running.

```python
python api_post_request_example.py
```

## Via Submitting Post Request with cURL

Similar to previous method, we can also use curl command to pass a input JSON to the API. Please note that -d indicates the data, -H refers to the header and -X represents the type of requests. 

```linux
curl -d '{"text":"Barack Obama is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017."}' -H 'Content-Type: application/json' -X POST {YOUR_SERVICE_URL}
```

## Via Parameters:

We can also pass in the parameter directly in URL. In this case, we pass in a parameter called text. You need to modify the port number and urls based on where your service is running.

```linux
curl {YOUR_SERVICE_URL}?text=Barack%20Obama%20is%20an%20American%20politician%20and%20attorney%20who%20served%20as%20the%2044th%20president%20of%20the%20United%20States%20from%202009%20to%202017.
```

# Important Places you may Need to Modify for your Demo

## Step 1: Load your Model
Please load your model for annotations. For this template, we implements PoS and NER services from Spacy

for Spacy we implement the following script for installing and loading the model:

```linux
!python -m spacy download en_core_web_sm
```

```python
import spacy
model = spacy.load("en_core_web_sm")
r = model(text)
```

## Step 2: Modify the outputToJSON function

Please modify the outputToJSON function based on the behavior of your model. Your functions should contain more functionalities, including data validation, data pre-processing and/or other features.

## Step 3: Change the Ports and Urls for the Post Request and Backend Service Script
In this demo, we use the localhost:8081 port. You should choose another available port and modify it. Moreover, the corresponding url for the backend service files should be updated as well. 
