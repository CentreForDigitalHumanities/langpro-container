#!/usr/bin/env python
# -*- coding: utf8 -*-
# usage: python3 call.py

import requests, json
import sys, os
import argparse
from nltk import Tree, TreePrettyPrinter
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True) # resets colores for each print
header_sty = Style.BRIGHT + Fore.BLUE + Back.WHITE
compact_style = Style.BRIGHT + Fore.WHITE + Back.GREEN
str_style = Style.BRIGHT + Fore.WHITE + Back.BLACK
repr_style = Style.BRIGHT + Fore.WHITE + Back.BLUE
pretty_style = Style.BRIGHT + Fore.WHITE + Back.MAGENTA

current_dir = os.path.dirname(os.path.abspath(__file__))
langpro_python = os.path.join(current_dir, '../../LangPro/python/')
sys.path.append(langpro_python)
from langpro_api import parse_langpro_json, parse_ccg_tree, parse_term, \
                        parse_kb, tree_to_line, parse_info_proof


# sample NLI problems
sample_nli_problems = [
    {   'premises': [   "John runs"],
        'hypothesis':   "John moves"
    },    
    {   'premises': [   "All animals sleep"],
        'hypothesis':   "Every dog sleeps"
    },
    {   'premises': [   'Every man is working',
                        'Everybody who is working has an expensive car'],
        'hypothesis':   'Every man owns a car'
    },
    {   'premises': [   'A woman is putting on lipstick'],
        'hypothesis':   'There is no woman putting on lipstick'
    },
]

parser = argparse.ArgumentParser(description="Solve a problem by its ID.")

# specifying problem id
parser.add_argument("-p", "--pid",
    type=int, required=True,
    help=f"Problem id to solve from [0:{len(sample_nli_problems)}]"
)
# optionally specifying representation type
parser.add_argument("-r", "--rep",
    choices=["tree", "term", "corr_term", "llf", "proof", "all"],
    help=f"Choosing which particular representation to print",
    default="all"
)
parser.add_argument("-v", "--verbose",
    type=int, default=0,
    help=f"Verbosity level of reporting"
)
args = parser.parse_args()


url = "http://localhost:8080/api/prove/"
headers = {'Content-Type': 'application/json'}

default_parameters = { 'prover_config': ['allInt', 'aall'],
                'ral': 200,
                'senses': 'all',
                'v': 1 }

inputs = [ {**p, **default_parameters} for p in sample_nli_problems ]
sample_nli = inputs[args.pid]

response = requests.post(url, headers=headers, data=json.dumps(sample_nli))

print("Status Code:", response.status_code)
print("Response text type:", type(response.text))
print("Response text length:", len(response.text))


try:
    output = json.loads(response.text)
    if args.verbose > 0:
        print(f"response.text:\n{response.text[:100]}\n\n")
except:
    print(f"response.text:\n{response.text[:100]}\n\n")
    raise

# print NLI problem
print(f"\n{header_sty}NLI problem")
sentences = [ i['sen'] for i in output['prob'] if i['role'] in 'ph' ]
for i, sen in enumerate(sentences[:-1], start=1):
    print(f"P{i}: {sen}")
print(f"H : {sentences[-1]}")

# print KB
print(f"\n{header_sty}KB relations")
for rel in parse_kb(output['kb']):
    print(rel)

# print CCG derivations for all sentences
if args.rep in ["tree", "all"]:
    print(f"\n{header_sty}CCG derivations")
    print(f"\n{header_sty}CCG derivations")
    ccg_trees = [ parse_ccg_tree(i['tree']['ccg_tree']) for i in output['prob'] ]
    for i in ccg_trees:
        print(f"{str_style}{tree_to_line(i)}")
        print(f"{pretty_style}{TreePrettyPrinter(i).text()}")

# print CCG terms for all sentences
if args.rep in ["term", "all"]:
    print(f"\n{header_sty}CCG terms")
    ccg_terms = [ parse_term(i['tree']['ccg_term']) for i in output['prob'] ]
    for i in ccg_terms:
        print(f"{compact_style}{i.compact()}")
        print(f"{str_style}{i}")
        print(f"{repr_style}{repr(i)}")
        print(f"{pretty_style}{i.pretty_printer().text()}")

# print Corrected terms (i.e. they are proper lambda terms) for all sentences
if args.rep in ["corr_term", "all"]:
    print(f"\n{header_sty}Corrected terms")
    corr_terms = [ parse_term(i['tree']['corr_term']) for i in output['prob'] ]
    for i in corr_terms:
        print(f"{compact_style}{i.compact()}")
        print(f"{str_style}{i}")
        print(f"{repr_style}{repr(i)}")
        print(f"{pretty_style}{i.pretty_printer().text()}")

# print LLFs (lambda terms with type-raised NPs) for all sentences
if args.rep in ["llf", "all"]:
    print(f"\n{header_sty}Lambda Logical Forms (LLFs)")
    llfs = [ parse_term(i['tree']['llf']) for i in output['prob'] ]
    for i in llfs:
        print(f"{compact_style}{i.compact()}")
        print(f"{str_style}{i}")
        print(f"{repr_style}{repr(i)}")
        print(f"{pretty_style}{i.pretty_printer().text()}")

# print tableau proofs
if args.rep in ["proof", "all"]:
    print(f"\n{header_sty}--- Tableau proofs ---")
    lab_proofs = [ (label, parse_info_proof(info_proof)) \
                    for label, info_proof in output['proofs'].items() ]
    for label, proof in lab_proofs:
        print(f"\n\t{header_sty}Proof tree for {label}")
        print(f"{pretty_style}{TreePrettyPrinter(proof).text()}")