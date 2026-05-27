"""
Tests for api functions.
The test cases are based on 3 NLI problems, which are represented in
a more readable format in NLI_PROBLEMS, and also in the prolog json format
in data/nli_prob{0,1,2}.json files.
The expected values for the tests are in data/expected.json,
which are also based on the same 3 NLI problems.
"""

import pytest
import sys
from nltk import Tree
import json
from pathlib import Path

# importing langpro_api functions
LANGPRO_PY = Path(__file__).resolve().parents[3] / "LangPro/python"
# Check the availability of the api file
if not (LANGPRO_PY / 'langpro_api.py').is_file():
    raise RuntimeError(f"Couldn't find langpro_api.py in {LANGPRO_PY}")
sys.path.insert(0, str(LANGPRO_PY))
from langpro_api import parse_ccg_tree, parse_term, parse_proof_tree

# importing container api functions
DEMO_DIR = Path(__file__).resolve().parents[1]
if not (DEMO_DIR / 'server.py').is_file():
    raise RuntimeError(f"Couldn't find server.py in {DEMO_DIR}")
sys.path.insert(0, str(DEMO_DIR))
from server import serialize_tree

DATA_DIR = Path(__file__).parent / "data"


####################################################
############# Sample NLI problems ##################
# more readable nli problems than json files
NLI_PROBLEMS = [
    {   'premises': [   "John runs"],
        'hypothesis':   "John moves"
    },
    {   'premises': [   "All animals sleep"],
        'hypothesis':   "Every dog sleeps"
    },
    {   'premises': [   "Every man is working",
                        "Everybody who is working has an expensive car"],
        'hypothesis':   "Every man owns a car"
    },
]

# read the content of nli_prob{0,1,2}.json files, which serves as input to tests
NLI_PROB_LP_JSON = {}
for i in range(3):
    with open(DATA_DIR / f"nli_prob{i}.json", encoding="utf-8") as F:
        out = json.load(F)
        # check consistency with NLI_PROBLEMS
        assert NLI_PROBLEMS[i]['premises'] == \
            [e["sen"] for e in out["prob"] if e["role"] == "p"]
        assert NLI_PROBLEMS[i]['hypothesis'] == \
            [e["sen"] for e in out["prob"] if e["role"] == "h"][0]
        NLI_PROB_LP_JSON[f"prob{i}"] = out

# read all the expected values
with open(DATA_DIR / "expected.json", encoding="utf-8") as F:
    EXPECTED = json.load(F)

####################################################
##################### TESTS ########################

# 28 tests
@pytest.mark.parametrize("prob_id, sen_idx, tree_type",
    [
        (prob_id, sen_idx, tree_type)
        for prob_id in [0, 1, 2]
            for sen_idx, _ in enumerate(NLI_PROB_LP_JSON[f"prob{prob_id}"]["prob"])
                for tree_type in ["ccg_tree", "ccg_term", "corr_term", "llf"]
    ])
def test_serialize_tree_for_trees(prob_id, sen_idx, tree_type):
    """ Test serialize_tree for sentence-level tree structures
    Input: sentence identifier (problem id, sentence position),
        and the type of tree/term (ccg_tree, ccg_term, corr_term, or llf).
    Expected: the serialized tree structure in dict format from expected.json.
    """
    pid = f"prob{prob_id}"

    # get right input for a sentences and its tree/term
    json_sen = NLI_PROB_LP_JSON[pid]["prob"][sen_idx]
    json_tree = json_sen["tree"][tree_type]

    # get right expected value for a sentences and its tree/term
    expected_sen = [ s for \
        s in (EXPECTED[pid]['p'] + [EXPECTED[pid]['h']]) \
        if s["sen"] == json_sen["sen"]][0]
    expected = expected_sen[f"serialized_{tree_type}"]
    # for intermediate checking of parsing
    expected_repr_parsed = expected_sen[f"repr_{tree_type}"]

    # parse the json tree into nltk tree or TT object
    if tree_type == "ccg_tree":
        nltk_tree = parse_ccg_tree(json_tree)
        # do intermediate checking for the correctness of parsing
        assert repr(nltk_tree) == expected_repr_parsed
    else:
        term = parse_term(json_tree)
        # do intermediate checking for the correctness of parsing
        assert repr(term) == expected_repr_parsed
        nltk_tree = term.tree()

    # main assertion
    serialized = serialize_tree(nltk_tree)
    assert serialized == expected


# 6 tests
@pytest.mark.parametrize("prob_id, label",
    [ (prob_id, label)
        for prob_id in range(3)
            for label in ["entailment", "contradiction"]
    ])
def test_serialize_tree_for_proofs(prob_id, label):
    """ tests serialize_tree for ent. and cont. poofs trees per problem
    Input: proof tree in prolog json format, that is on-fly parsed into nltk Tree
    Expected: the serialized tree structure in dict format from expected.json.
    """
    pid = f"prob{prob_id}"
    json_proof = NLI_PROB_LP_JSON[pid]["proofs"][label]["proof"]

    # on the fly parse the proof json to nltk Tree and check the correctness
    proof_tree = parse_proof_tree(json_proof)
    assert repr(proof_tree) == EXPECTED[pid][f"repr_{label}"]

    serialized = serialize_tree(proof_tree)
    print(json.dumps(serialized, ensure_ascii=False), end="\n\n\n")
    expected = EXPECTED[pid][f"serialized_{label}"]
    assert serialized == expected


if __name__ == "__main__":
    # for debugging
    pass