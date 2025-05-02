from flask import Flask, request

import langpro_demo as lp
from util import run_tool

app = Flask(__name__)

LANGPRO_EXE = "nat_lang_pro/langpro"
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


def get_goal(parser, config, user_input=False):
    (sen_pl, spl) = lp.user_input_to_pl_spl(kw["input"])
    kw["sen_pl"] += sen_pl
    # parsing sentences with easyCCg and C&C
    ders = lp.ccg_parsing(parser, spl)
    pl_facts = kw["sen_pl"] + ders
    assert_cl = lp.assertz_clause(pl_facts)
    return ' -g "{0}, {1}, online_demo(1), halt"'.format(assert_cl, kw["config"])


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


def langpro_raw(goal):
    # cmd = ['swipl', '-x', LANGPRO_EXE, goal]
    cmd = "swipl -x {} {} ".format(LANGPRO_EXE, goal)
    proof = run_tool(cmd)
    return "<doc>" + process_proof(proof) + "</doc>"


@app.route("/foo/", methods=["POST"])
def test():
    if request.json is None:
        raise RuntimeError()

    config = request.json["prover_config"]
    premises = [premise.replace("'", "\\'") for premise in request.json["premises"]]
    hypothesis = request.json["hypothesis"].replace("'", "\\'")
    ral = request.json["ral"]
    senses = request.json["senses"]

    # format user input for prolog
    sentences = (
        ":- dynamic sen_id/5.\n"
        ":- multifile sen_id/5.\n"
        ":- discontiguous sen_id/5.\n\n"
    )
    for i, premise in enumerate(premises):
        sentences += "sen_id({0}, 1, '{1}', 'nil', '{2}').\n".format(
            i + 1, "p", premise
        )
    sentences += "sen_id({0}, 1, '{1}', 'nil', '{2}').\n".format(
        len(premises) + 1, "h", hypothesis
    )

    eff_cr = "effCr([equi, nonBr, nonProd, nonCons])"
    wn_rel = "wn_ant, wn_der, wn_sim"
    senses = "" if senses == "all" else "ss({})".format(senses)
    allInt_aall = ", ".join(config) if config else ""
    kw_config = f" parList([proof_tree, pr_kb, {eff_cr}, {wn_rel}, ral({ral}), {senses} {allInt_aall}])"

    # send input to parser
    sentences_for_parser = "\n".join(premises + [hypothesis])
    derivations = lp.ccg_parsing("cc", sentences_for_parser)

    facts = sentences + derivations
    assert_cl = lp.assertz_clause(facts)
    goal = ' -g "{0}, {1}, online_demo(1), halt"'.format(assert_cl, kw_config)
    return langpro_raw(goal)


@app.route("/user/")
def process_user():
    config = lp.security_clean(request.args.getlist("prover_config"))
    input = lp.security_clean(request.args.get("rte_problem", ""))
    parsers = lp.security_clean(request.args.getlist("parser"))
    ral = lp.security_clean(request.args.get("ral"))
    senses = lp.security_clean(request.args.get("senses"))
    sen_pl = (
        ":- dynamic sen_id/5.\n"
        ":- multifile sen_id/5.\n"
        ":- discontiguous sen_id/5.\n\n"
    )

    _sen_pl, spl = lp.user_input_to_pl_spl(input)
    sen_pl += _sen_pl

    eff_cr = "effCr([equi, nonBr, nonProd, nonCons])"
    wn_rel = "wn_ant, wn_der, wn_sim"
    senses = "" if senses == "all" else "ss({})".format(senses)
    allInt_aall = ", ".join(config) if config else ""
    kw_config = f" parList([proof_tree, pr_kb, {eff_cr}, {wn_rel}, ral({ral}), {senses} {allInt_aall}])"

    goal_dict = {}
    for parser in parsers:
        derivations = lp.ccg_parsing(parser, spl)
        pl_facts = sen_pl + derivations
        assert_cl = lp.assertz_clause(pl_facts)
        goal_dict[parser] = ' -g "{0}, {1}, online_demo(1), halt"'.format(
            assert_cl, kw_config
        )

    results = []
    for parser in parsers:
        swipl_goal = goal_dict[parser]
        results.append(lp.run_langpro(parser, LANGPRO_EXE, swipl_goal))
    return format_results(results)


@app.route("/sick/")
def process_sick():
    config = lp.security_clean(request.args.getlist("prover_config"))
    input = lp.security_clean(request.args.get("rte_problem", ""))
    parsers = lp.security_clean(request.args.getlist("parser"))
    ral = lp.security_clean(request.args.get("ral"))
    senses = lp.security_clean(request.args.get("senses"))
    prob_id = lp.security_clean(request.args.get("prob_id"))
    sen_pl = (
        ":- dynamic sen_id/5.\n"
        ":- multifile sen_id/5.\n"
        ":- discontiguous sen_id/5.\n\n"
    )

    _sen_pl, spl = lp.user_input_to_pl_spl(input)
    sen_pl += _sen_pl

    eff_cr = "effCr([equi, nonBr, nonProd, nonCons])"
    wn_rel = "wn_ant, wn_der, wn_sim"
    senses = "" if senses == "all" else "ss({})".format(senses)
    allInt_aall = ", ".join(config) if config else ""
    kw_config = f" parList([proof_tree, pr_kb, {eff_cr}, {wn_rel}, ral({ral}), {senses} {allInt_aall}])"
    data_name = "SICK_train_sen"
    goal = ' -g "{0}, online_demo({1}), halt" -l {2}/{3}'.format(
        kw_config, prob_id, RTE_PROB_DIR, data_name
    )

    results = []
    for parser in parsers:
        swipl_goal = "{0}_{1}.pl".format(goal, lp.str_map(parser, mode="ext"))
        results.append(lp.run_langpro(parser, LANGPRO_EXE, swipl_goal))
    return format_results(results)


@app.route("/fracas/")
def process_fracas():
    data_name = "fracas_sen_d"
    return "fracas result"


@app.route("/")
def index():
    return "hello from flask"


def main():
    app.run()


if __name__ == "__main__":
    main()
