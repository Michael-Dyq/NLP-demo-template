'''
This script serves to call an API request on the Multilingual NER Demo on port 4033 
'''

import requests
import json

# The target URL where we send to request to
#url = 'http://localhost:8081/anns'
url = 'http://dickens.seas.upenn.edu:8099/anns'

# The parameters we wish to send
json_in = {
        'text' : 'Barack Obama is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017.'
        }

# Set the headers for the request
headers = {'content-type': 'application/json'}

# Post the request
json_out = requests.post(url, data = json.dumps(json_in), headers=headers)

# Retrieve the JSON of the Output
res = json_out.json()

# Print the response text (the content of the requested file):
print(json.dumps(res))