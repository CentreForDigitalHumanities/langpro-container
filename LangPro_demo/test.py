#!/usr/bin/env python
# -*- coding: utf8 -*-
# usage: python3 test.py

import argparse
import sys, os
import nltk

# importing langpro_api functions
# #TODO: find a better way to import these functions
current_dir = os.path.dirname(os.path.abspath(__file__))
langpro_python = os.path.join(current_dir, '../../LangPro/python/')
# Check the availability of the api file
if not os.path.isfile(f"{langpro_python}/langpro_api.py"):
    raise RuntimeError(f"Couldn't find langpro_api.py in {langpro_python}")
sys.path.append(langpro_python)
from langpro_api import parse_ccg_tree, parse_term, \
                        parse_kb, tree_to_line, parse_info_proof, \
                        PrologTerm

#################### Argument parsing ################
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("test", nargs="?",
        help="Name of one test to run. If omitted, run all tests.",
    )
    parser.add_argument("--list", action="store_true",
        help="List available tests and exit.",
    )
    # specifying problem id of the predefined toy problems
    parser.add_argument("-i", "--pid",
        type=int, required=False, metavar='PROBLEM_ID',
        help=f"Problem id to solve, in range [0:{len(sample_nli_problems)-1}]"
    )

    args = parser.parse_args()
    if args.test is not None and args.test not in TESTS:
        parser.error(f"Unknown test: {args.test!r}")
    return args


####################################################
############# Sample NLI problems ##################
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
]

####################################################
################### test functions #################
# #TODO perhaps needs a better way to import these
def serialize_tree(tree: nltk.Tree, out=None):
    if out is None:
        out = dict()

    if isinstance(tree, PrologTerm):
        out["node"] = [str(arg) for arg in tree.args]
        return out

    out["node"] = tree.label()
    out["children"] = []
    for child in tree:
        root = dict()
        out["children"].append(root)
        serialize_tree(child, root)

    return out


####################################################
############### Utility functions ##################
def check(name, fn, args):
    """ A wrapper function for checking the result of a test function
    """
    try:
        fn(args)
        print(f"[OK]    {name}")
    except AssertionError as e:
        print(f"[FAIL]  {name}")
        if e:
            print(f"       {e}")
        raise
    except Exception as e:
        print(f"[ERR]   {name}: {type(e).__name__}: {e}")
        raise


def assert_equal(got, expected, msg=""):
    """ Wrapper for assert 
    """
    assert got == expected, (msg or f"expected {expected!r}, got {got!r}")


def langpro_api_call(premises, hypothesis,
                     endpoint="http://localhost:8080/api/prove/",
                     parser="easyccg", ral=200, kb=[], senses = 'all',
                     strong_align=True, intersective=True, curl=False, report=False):
    """ Uses API call to a remote server to run LangPro prover
        and get parsed input sentecnes, tableau proof, and inference label.
        :param premises: list of premises
        :param hypothesis: hypothesis
        :param endpoint: endpoint of the server
        :param parser: CCG parser's name that will be used ("cc", "re-cc", or "easyccg")
        :param ral: rule applciation limit
        :param kb: user-injected knowledge base, a list of lexical relations
        :param senses: number of word senses used per word
        :param strong_align: whether to align indefinite NPs
        :param intersective: whether to treat modifiers by default as intersective
        :param curl: whether to print curl command
        :param report: whether to print error-related report
        :return: a dictionary with parsed input sentences, tableau proof, and inference label
    """
    import json, requests
    # preparing an input for the API call
    prob = {'premises': premises, 'hypothesis': hypothesis}
    headers={'Content-Type': 'application/json'}
    parameters = {  'prover_config': [],
                    'parser': parser,
                    'ral': ral,
                    'kb': kb,
                    'senses': senses    }
    if strong_align: parameters['prover_config'].append('aall')
    if intersective: parameters['prover_config'].append('allInt')
    query = {**prob, **parameters}
    js_query = json.dumps(query)

    # optinal, for curl command
    if curl:
        curl_command = f"curl '{endpoint}' " +\
        " ".join([f"-H '{k}: {v}'" for k, v in headers.items()]) +\
        f" -d '{js_query}'"
        print(curl_command)

    response = requests.post(endpoint, data=js_query, headers=headers)
    try:
        output = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        if report:
            print(f"Failed to parse JSON response")
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response text: {response.text[:20]}")  # First 20 chars
            print(f"Error: {e}")
        return None

    # parsing the components of the output
    kb = parse_kb(output['kb'])
    ccg_trees = [ parse_ccg_tree(i['tree']['ccg_tree']) for i in output['prob'] ]
    ccg_terms = [ parse_term(i['tree']['ccg_term']) for i in output['prob'] ]
    corr_terms = [ parse_term(i['tree']['corr_term']) for i in output['prob'] ]
    llfs = [ parse_term(i['tree']['llf']) for i in output['prob'] ]
    lab_proofs = { label: parse_info_proof(info_proof) \
                    for label, info_proof in output['proofs'].items() }
    # derive a predicted inference label
    entailment = 'closed' in output["proofs"]["entailment"]["info"]
    contradiction = 'closed' in output["proofs"]["contradiction"]["info"]
    if entailment and not contradiction:
        label = 'entailment'
    elif not entailment and contradiction:
        label = 'contradiction'
    else:
        label = 'neutral'
    # wrap up all in a dict
    return {'kb':kb, 'ccg':ccg_trees, 'ccg_terms':ccg_terms, 'label':label,
            'terms':corr_terms, 'llfs':llfs, 'proofs':lab_proofs}

####################################################
##################### TESTS ########################

def test_serialize_ccgtree_leaves_similarly(args):
    pid = args.pid if args.pid is not None else 0
    nli_prob = sample_nli_problems[pid]
    prems, hypo = nli_prob['premises'], nli_prob['hypothesis']
    out = langpro_api_call(prems, hypo)

    ser_ccg = [ serialize_tree(t) for t in out["ccg"] ]
    ser_ccg_terms = [ serialize_tree(t.tree()) for t in out["ccg_terms"] ]
    ser_terms = [ serialize_tree(t.tree()) for t in out["terms"] ]
    ser_llfs = [ serialize_tree(t.tree()) for t in out["llfs"] ]

    pass
    
    #     ccg_parses = [
    #     {
    #         "sentence": entry["sen"],
    #         "ccg_trees": {
    #             "ccg_tree": serialize_tree(parse_ccg_tree(entry["tree"]["ccg_tree"])),
    #             "ccg_term": serialize_tree(parse_term(entry["tree"]["ccg_term"]).tree()),
    #             "corr_term": serialize_tree(parse_term(entry["tree"]["corr_term"]).tree()),
    #             "llf": serialize_tree(parse_term(entry["tree"]["llf"]).tree()),
    #         },
    #     }
    #     for entry in raw["prob"]
    # ]

    # assert_equal(got, 5)


####################################################


TESTS = {
    name[5:]: fn 
        for name, fn in globals().items()
        if name and name.startswith("test_") and callable(fn)
}


def main():
    args = parse_arguments()

    # printing available tests and exiting
    if args.list:
        print("Available tests:")
        for name in TESTS:
            print(f"\t{name}")
        return

    # Running a specific test
    if args.test:
        check(args.test, TESTS[args.test], args)
        print("\nSelected test passed.")
        return

    # Running all tests
    for name, fn in TESTS.items():
        check(name, fn)
    print("\nAll tests passed.")


if __name__ == "__main__":
    main()