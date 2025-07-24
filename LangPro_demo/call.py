#!/usr/bin/env python
# -*- coding: utf8 -*-
# usage: python3 call.py

import requests, json
import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
langpro_python = os.path.join(current_dir, '../../LangPro/python/')
sys.path.append(langpro_python)

from langpro_api import from_json, ccg_tree_to_tree

url = "http://localhost:8080/api/foo/"
headers = {'Content-Type': 'application/json'}
input1 = {'prover_config': ['allInt', 'aall'], 
         'premises': ['Every man is working', 
                      'Everybody who is working has an expensive car'], 
          'hypothesis': 'Every man owns a car', 
          'ral': 200, 
          'senses': 'all', 
          'v': 1
        }
input2 = {'prover_config': ['allInt', 'aall'], 
         'premises': ["All animals sleep"], 
         'hypothesis': "Every dog sleeps",
         'ral': 200, 
         'senses': 'all', 
         'v': 1
        }

response = requests.post(url, headers=headers, data=json.dumps(input1))

print("Status Code:", response.status_code)
print("Response text type:", type(response.text))
print("Response text length:", len(response.text))

output = json.loads(response.text)

print("\nNLI problem")
sentences = [ i['sen'] for i in output['prob'] if i['role'] in 'ph' ]
for i, sen in enumerate(sentences[:-1], start=1):
    print(f"P{i}: {sen}")
print(f"H : {sentences[-1]}")

print("\nCCG derivations")
ccg_trees = [ from_json(i['tree']['ccg_tree']) for i in output['prob'] ]
ccg_trees = map(ccg_tree_to_tree, ccg_trees)
for i in ccg_trees:
    i.pretty_print()