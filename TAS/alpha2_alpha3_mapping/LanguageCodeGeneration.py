import pycountry
import json

alpha2ToAlpha3 = {}
alpha3ToAlpha2 = {}
lst = []

# print(len(pycountry.languages))
# print(list(pycountry.languages)[0])

# Note: cannot directly load to dict; it generates getAttr error 
for lang in list(pycountry.languages):
     if hasattr(lang, 'alpha_2') and hasattr(lang, 'alpha_3'):
         lst.append((lang.alpha_2, lang.alpha_3))

for alpha2, alpha3 in lst:
    alpha3ToAlpha2[alpha3] = alpha2
    alpha2ToAlpha3[alpha2] = alpha3

with open('alpha2Toalpha3.txt', 'w') as file:
     file.write(json.dumps(alpha2ToAlpha3)) # use `json.loads` to do the reverse

with open('alpha3Toalpha2.txt', 'w') as file:
     file.write(json.dumps(alpha3ToAlpha2)) 