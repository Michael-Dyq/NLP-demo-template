'''
This script serves to call an API request on the Multilingual NER Demo on port 4033 
'''

import requests
import json

# The target URL where we send to request to
url_pos = 'http://dickens.seas.upenn.edu:4034/pos'
url_ner = 'http://dickens.seas.upenn.edu:4033/ner'

# The parameters we wish to send
json_pos = {
        'text' : 'Barack Obama is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017.'
        }

json_ner = {
        'lang': 'eng',
        'model': 'bert',
        'text' : 'Barack Obama is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017.'
        }
# Set the headers for the request
headers = {'content-type': 'application/json'}

# Post the request
output_pos = requests.post(url_pos, data = json.dumps(json_pos), headers=headers)
output_ner = requests.post(url_ner, data = json.dumps(json_ner), headers=headers)

# Merge the output by their service tags
res = {
    "pos_anns" : output_pos.json(),
    "ner_anns" : output_ner.json()
}


# Print the response text (the content of the requested file):
print(res)