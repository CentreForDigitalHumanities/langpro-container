import json
import re
import nltk
from flask import Flask, request
from functools import lru_cache

import langpro_demo as lp

from langpro_api import (
    parse_ccg_tree, parse_info_proof, PrologTerm, Atom
)

from util import run_tool

app = Flask(__name__)

LANGPRO_BIN = "nat_lang_pro/langpro_bin"
RTE_PROB_DIR = "rte_problems"


def tabs_template(logs, tabs, final_answer, parsed, tab_content):
    return f"""
    <div class="tabs">
        <span>A tableau is built for each pair of <b>Relation</b> &amp; <b>Parser</b>.
            <i onclick="toggle_block('message_log')" class="fa fa-exclamation-triangle"
                style="color:red; font-size: 130%"></i>
            If a tableau proof is large it might not be visible at first.
            Zoom out or navigate to the right side to view tableau proofs.
        </span>
        <div id="message_log" style="display:none">{logs}</div>
        <ul class="tab-links">
        <li class="active"><a href="#summary">Summary</a></li>
        {tabs}</ul>
        <div class="tab-content">
            <div id="summary" class="tab active">
                <div>
                {final_answer}
                <i class="fa fa-info-circle"/></i>For each CCG parser and sentence:
                CCG derivation <i class="fa fa-arrow-right"></i>CCG term <i class="fa fa-arrow-right"></i>corrected CCG term <i class="fa fa-arrow-right"></i>the first LLF.
                Hover <i class="fa fa-mouse-pointer"></i>over categories/types
                to highlighting constituents.
                </div>
                {parsed}
            </div>
            {tab_content}
        </div>
    </div>
    """


def prepare_config(config, senses, ral):
    eff_cr = "effCr([equi, nonBr, nonProd, nonCons])"
    wn_rel = "wn_ant, wn_der, wn_sim"
    senses = "" if senses == "all" else "ss({})".format(senses)
    allInt_aall = ", ".join(config) if config else ""
    return f" parList([proof_tree, {eff_cr}, {wn_rel}, ral({ral}), {senses} {allInt_aall}])"

def str_to_quoted_atom(s):
    return  "'" + s.replace("'", "\\'") + "'"

def prepare_kb(kb):
    def prepare_rel(rel):
        assert isinstance(rel, str)
        pattern = re.compile(r"(isa_wn|ant_wn|disj)\(([^,]+),\s*([^,]+)\)")
        if (m := pattern.match(rel.strip())):
            pred, arg1, arg2 = m.groups()
            return f"{pred}({str_to_quoted_atom(arg1)}, {str_to_quoted_atom(arg2)})"
        else:
            raise ValueError(f"Cannot parse relation: {rel}")

    rels = [prepare_rel(rel) for rel in kb]
    return "[" + ', '.join(rels) + "]"


def prepare_input(input, parser):
    defs = (
        ":- dynamic sen_id/5.\n"
        ":- multifile sen_id/5.\n"
        ":- discontiguous sen_id/5.\n\n"
    )
    sentences_pl, sentence_per_line = lp.user_input_to_pl_spl(input)
    derivations = lp.ccg_parsing(parser, sentence_per_line)

    return defs + sentences_pl + derivations


def prepare_input_json(premises, hypothesis, parser, v=0):
    defs = (
        ":- dynamic sen_id/5.\n"
        ":- multifile sen_id/5.\n"
        ":- discontiguous sen_id/5.\n\n"
    )

    sentences_escaped = []
    sentences_pl = []
    input = [(premise, "p") for premise in premises] + [(hypothesis, "h")]

    # indices should match the ccg indices
    for idx, (sentence, type_) in enumerate(input, start=1):
        tokenized = " ".join(nltk.word_tokenize(sentence))
        escaped = tokenized.replace("'", "\\'")
        sentences_escaped.append(escaped)
        sentences_pl.append(
            "sen_id({0}, 1, '{1}', 'nil', '{2}').\n".format(idx, type_, escaped)
        )

    derivations = lp.ccg_parsing(parser, "\n".join(sentences_escaped), v=v)

    return "\n".join(defs) + "\n".join(sentences_pl) + derivations


def get_goal(facts, kb, config):
    assert_cl = lp.assertz_clause(facts)
    # json args are text width, indent step size, and tab size
    return ' -g "{0}, {1}, online_demo(1, {2}, json(0,1,1)), halt"'.format(assert_cl, config, kb)


def format_results(results):
    answers = "\n".join([res["answer"] for res in results])
    fanswers = "\n".join([res["fanswer"] for res in results])
    logs = "\n".join([res["log"] for res in results])
    tabs = "\n".join([res["tabs"] for res in results])
    parsed = "\n".join([f"<div>{res['parsed']}</div>" for res in results])
    tab_content = "\n".join([res["tab_content"] for res in results])

    final_answer = lp.aggregate_answers(answers)
    final_answer = (
        ' <div class="printed_answers_final"><i class="fa fa-legal"></i>'
        " <b>LangPro</b> thinks that the argument is"
        ' <span class="langpro_answer">{0}</span>.'
        " The judgement is based on its sub-decision(s):</div> {1}"
    ).format(final_answer, fanswers)
    return tabs_template(logs, tabs, final_answer, parsed, tab_content)


def process_proof(proof):
    return proof


@lru_cache  # meant for speeding up results during development
def langpro_raw(goal):
    cmd = "swipl -x {} {} ".format(LANGPRO_BIN, goal)
    proof = run_tool(cmd)
    return process_proof(proof)


def serialize_tree(tree: nltk.Tree, out=None):
    if out is None:
        out = dict()

    if isinstance(tree, PrologTerm):
        out["node"] = [str(arg) for arg in tree.args]
        return out

    if type(tree) == str:
        out["node"] = tree
        return out

    out["node"] = tree.label()
    out["children"] = []
    for child in tree:
        root = dict()
        out["children"].append(root)
        serialize_tree(child, root)

    return out


@app.route("/prove/", methods=["POST"])
def parse_and_prove():
    if request.json is None:
        raise RuntimeError()

    format = request.json.get("format", "raw")
    parser = request.json.get("parser", "cc")
    prover_config = request.json["prover_config"]
    premises = request.json["premises"]
    hypothesis = request.json["hypothesis"]
    ral = request.json["ral"]
    senses = request.json["senses"]
    kb = request.json.get("kb", [])
    # print("keys", request.json.keys())
    # verbosity level
    if "v" in request.json:
        v = request.json["v"]
    else:
        v = 0

    prover_config = prepare_config(prover_config, senses, ral)
    facts = prepare_input_json(premises, hypothesis, parser, v=v)
    kb = prepare_kb(kb)
    goal = get_goal(facts, kb, prover_config)
    if v > 0:
        print(f"swipl goal={goal}")
    raw = json.loads(langpro_raw(goal))

    if format == "raw":
        return raw

    prob = raw["prob"]
    ccg_trees = [entry["tree"]["ccg_tree"] for entry in prob]

    return dict(
        ccg_trees=[serialize_tree(parse_ccg_tree(tree)) for tree in ccg_trees],
        proofs={
            key: serialize_tree(parse_info_proof(value))
            for key, value in raw["proofs"].items()
        }
    )


def main():
    app.run(debug=True)
    # app.run()


if __name__ == "__main__":
    main()
