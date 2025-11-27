#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import argparse
import subprocess
import re
from pprint import pprint, pformat
import nltk
import lxml.etree as ET
from io import StringIO
from datetime import datetime
import os.path as op
import codecs
from util import run_tool



#################################
def parse_arguments():
    '''read arguments fed from the terminal (used for debuging)'''
    parser = argparse.ArgumentParser(description ='''Read a cgi arguments''')
    # input data
    parser.add_argument(
    '--rte-problem', default='', help='user input RTE problem')
    parser.add_argument(
    '--prob-id', default='', help='problem ID')
    parser.add_argument(
    '--data-type', default='', help='dataset name')
    parser.add_argument(
    '--senses', default='', help='the number of senses to be considered')
    parser.add_argument(
    '--parsers', default=['easyccg', 'cc'], nargs='+', help='the parser name')
    parser.add_argument(
    '--ral', default='', help='rule application limit')
    parser.add_argument(
    '--prover-config', default=['allInt', 'aall'], nargs='+', help='Other proof parameters')
    parser.add_argument(
    '--terminal', action='store_true', help='If it is run from terminal')
    return parser.parse_args()


#################################
def str_map(parser, mode='abbr'):
    '''Encodes abbreviation of the input'''
    abbr = {'easyccg':'easy',
            'cc':'cc'}
    ext = {'easyccg':'eccg',
           'cc':'ccg'}
    cap = {'easyccg':'EasyCCG',
           'cc':'C&amp;C'}
    if mode == 'abbr':
        return abbr[parser]
    elif mode == 'ext':
        return ext[parser]
    else:
        return cap[parser]


#################################
def run_langpro(parser, langpro, goal):
    abbr_parser = str_map(parser)
    cap_parser = str_map(parser, mode='cap')
    ok_parse, log, parsed, kb, ent_proof, cont_proof = langpro_to_html(langpro, goal)
    parsed = re.sub('(<div class="parsed_problem_title">Problem \d+:).+?(</div>)',
                    r'\1 parsed with {}\2'.format(cap_parser), parsed)
    if ok_parse:
        tabs = ('<li><a href="#tab_{0}_ent"> Entailment &amp; {1}</a></li>'
                '<li><a href="#tab_{0}_cont">Contradiction &amp; {1}</a></li>'
               ).format(abbr_parser, cap_parser)
        ent_info = tableau_info( ent_proof['align'], ent_proof['status'],
                                     ent_proof['apps'], kb )
        cont_info = tableau_info( cont_proof['align'], cont_proof['status'],
                                      cont_proof['apps'], kb )
        tab_content = ('<div id="tab_{0}_ent" class="tab">{1}\n{2}</div>'
                       '<div id="tab_{0}_cont" class="tab">{3}\n{4}</div>'
                      ).format(abbr_parser, ent_info, ent_proof['tableau'],
                               cont_info, cont_proof['tableau'])
        error_info = ''
    else:
        tab_content = tabs = ''
        if ent_proof and cont_proof:
            error_info = ('<span class="wrong_parse"><i class="fa fa-thumbs-down">'
                          '</i>due to inconsistent CCG categories!</span>')
        else: #parser couldnt parse anything
            error_info = ('<span class="wrong_parse"><i class="fa fa-thumbs-down">'
                          '</i>Parsing failed</span>')
            ent_proof['answer'] = cont_proof['answer'] = 'NA'
    # make final decision on inference class
    ans = aggregate_answers([ent_proof['answer'], cont_proof['answer']])
    html_ans = (
        ' <div class="printed_answers"><i class="fa fa-user-secret"></i>'
        ' Based on the <b>{4}</b> derivations, the argument is'
        ' <span class="parser_answer">{0}</span>'
        ' (<span class="tableau_answer">{1}</span>'
        ' and <span class="tableau_answer">{2}</span>) {3}</div>'
        ).format(ans, ent_proof['answer'].lower(),
                 cont_proof['answer'].lower(), error_info, cap_parser)
    return {'parsed':parsed,
            'log':'<div class="message_log_{}">{}</div>'.format(abbr_parser, log),
            'tabs':tabs,
            'tab_content':tab_content,
            'answer':ans,
            'fanswer':html_ans}


#################################
def langpro_to_html(langpro, goal):
    '''Given a langpro path and a prolog loading and goal instructions,
       run langpro and return its html output and other details
    '''
    cmd = 'swipl -x {} {} '.format(langpro, goal)
    proof = run_tool(cmd)
    original_proof = proof
    #print '<xmp>{}</xmp>'.format(proof)
    # parser error while aprsing sentences (C&C)
    if re.search('ERROR:', proof):
        return (False, '', '', '', {}, {})
    ok_parse = False if re.search('Inconsistency in node types - generateTableau', proof)\
                     else True
    proof = pretty_G_variables(proof)
    # read output from the stdout
    #print '<xmp>proof length = {}</xmp>'.format(len(proof))
    #FIXME use xml parser
    #print '<pre>match object {}</pre>'.format(pformat(m))
    kb = re.search('KB:.*?\[(.*?)\]', proof).group(1)
    parsed_prob_xml = re.search('(<parsed_problem.+</parsed_problem>)',
                                proof, re.S).group(1)
    m = re.search('(<tableau>.*?</tableau>).*?(<tableau>.*?</tableau>).*?([a-zA-Z_\d]+).*?([a-zA-Z_\d]+)', proof, re.DOTALL)
    (tab_ent, tab_cont, ent_ans, cont_ans) = m.groups()
    #print '<pre>{}, {}, {}, {}, {}, {}</pre>'.format(kb, len(parsed_prob_xml), len(tab_ent), len(tab_cont), ent_ans, cont_ans)
    #parsed_prob_xml = re.sub('KB:', '', parsed_prob_xml, re.DOTALL)
    parsed_prob_xml = re.sub('(<parsed_problem.*?>).*?<parsed', r'\1<parsed', parsed_prob_xml, flags=re.DOTALL)  # delete possible KB
    #parsed_prob_xml = ''
    #print "<xmp>kb = {}</xmp>".format(kb)

    kb = re.sub('\),', '), ', kb)
    #kb = re.sub(r'\w+\((\w+),\1\),?', '', kb)
    kb = re.sub(',\s*$', '', kb)
    #print "<xmp>kb = {}</xmp>".format(kb)

    ############### XSL transformations ################
    ttterms_xsl = 'xml/ttterms.xsl'
    parsed_prob_html = xsl_transformation(parsed_prob_xml, ttterms_xsl)
    #parsed_prob_html = re.sub('^.*?(<div class="parsed_problem">.+</div>).*', r'\1', parsed_prob_html, flags=re.DOTALL)
    parsed_prob_html = re.sub('(Warning\: Sentence could not be parsed)', r'<span class="warning_no_parse">\1</span>', parsed_prob_html)
    # get details from both proofs
    #print "<xmp>{}\n{}</xmp>".format(ent_ans, cont_ans)
    ent_proof = proof_results(ok_parse, tab_ent, ent_ans)
    cont_proof = proof_results(ok_parse, tab_cont, cont_ans)

    ############### Read statuses of tableau proofs ################
    message_log = (
        '<p class="log_label">ent_ans and cont_ans from langpro</p>\n'
        '<pre>'+ent_ans+', '+cont_ans+'</pre>\n'
        '<p class="log_label">parsed ent_ans and cont_ans</p>\n'
        '<pre>('+ent_proof['answer']+', '+ent_proof['align']+','
        ' '+ent_proof['status']+', '+ent_proof['apps']+'); '
        '('+cont_proof['answer']+', '+cont_proof['align']+','
        ' '+cont_proof['status']+', '+cont_proof['apps']+')</pre>\n'
        '<p class="log_label">Command</p>\n'
        '<pre>'+cmd+'</pre>\n'
        '<p class="log_label">Parsed problem in XML</p>\n'
        '<xmp>'+parsed_prob_xml+'</xmp>\n'
        '<p class="log_label">Parsed problem in HTML</p>\n'
        '<xmp>'+parsed_prob_html+'</xmp>\n'
        '<p class="log_label">Entailment tableau in XML</p>\n'
        '<xmp>'+tab_ent+'</xmp>\n'
        '<p class="log_label">Entailment tableau in HTML</p>\n'
        '<xmp>'+ent_proof['tableau']+'</xmp>\n'
        '<p class="log_label">Contradiction tableau in XML</p>\n'
        '<xmp>'+tab_cont+'</xmp>\n'
        '<p class="log_label">Contradiction tableau in HTML</p>\n'
        '<xmp>'+cont_proof['tableau']+'</xmp>\n'
        '<p class="log_label">SWIPL proof with Nice G variables</p>\n'
        '<xmp>'+proof+'</xmp>\n'
        '<p class="log_label">Whole original proof from SWIPL</p>\n'
        '<xmp>'+original_proof+'</xmp>\n'
        '<p class="log_label">Knowledge</p>\n'
        '<pre>'+kb+'</pre>')
    #print '<xmp>{}; {}</xmp>'.format(ent, ent_al)
    return (ok_parse, message_log, parsed_prob_html, kb, ent_proof, cont_proof)

###############
def xsl_transformation_old(xml_data, xsl_path, depth=100000000):
    '''Apply an XSL file to transform an XML data
    '''
    # xslt_type = op.splitext(op.basename(xsl_path))[0]
    # timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
    # filename = 'xslt_junk/{}_{}.xml'.format(xslt_type, timestamp)
    # with codecs.open(filename, 'w', encoding='utf-8') as f:
    #     f.write(xml_data)
    # cmd = "xsltproc --maxparserdepth {0} --maxdepth {0} {1} {2}".format(
    #       depth, xsl_path, filename)
    # return run_tool(cmd)

    breakpoint()
    transform = ET.XSLT(ET.parse(xsl_path))
    out = ET.tostring(transform(ET.fromstring(xml_data))).decode()
    return out

###############
def xsl_transformation_x(xml_data, xsl_path, depth=100000000):
    '''Apply an XSL file to transform an XML data
    '''
    xsltproc =  "xsltproc --maxparserdepth {0} --maxdepth {0}".format(depth)
    # apply xslt to parsed problem
    cmd = ('{{\n cat <<HUGETEXT\n {} \nHUGETEXT\n}} | '
           '{} {} -').format(xml_data, xsltproc, xsl_path)
    cmd = ('{} {} <(\n cat <<HUGETEXT\n {} \nHUGETEXT\n)').format(xsltproc, xsl_path, xml_data)

    return run_tool(cmd)

###############
def xsl_transformation(xml_data, xsl_path, depth=100000000):
    '''Apply an XSL file to transform an XML data
    '''
    tableau_xml = ET.fromstring(xml_data)
    #print "xml root node: <xmp>{}</xmp>".format(tableau_xml.tag)
    #print "XML:\n<xmp>{}</xmp>".format(ET.tostring(tableau_xml, pretty_print=True))
    xslt = ET.parse(xsl_path)
    transform = ET.XSLT(xslt)
    #print "<xmp>{}</xmp>".format(type(transform))
    tableau_html = transform(tableau_xml)
    #print "html root node: {}".format(tableau_html.tag)
    out = ET.tostring(tableau_html).decode()
    out = re.sub('<!DOCTYPE .+?>.+?<body .+?>', '', out, flags=re.DOTALL)
    out = re.sub('</body>\s*</html>', '', out, flags=re.DOTALL)
    return out

###############
def proof_results(ok_parse, tab_xml, langpro_answer):
    '''Return a dictionary containing a tableau proof in html, and statuses of
       entailment, alignment, tableau and number of applied rules
    '''
    if ok_parse:
        tableau_xsl = 'xml/tableau.xsl'
        #print '<xmp>{}</xmp>'.format(tab_xml)
        tab_html = xsl_transformation(tab_xml, tableau_xsl)
        tab_html = re.sub('.*?(<span class="tree">.+</span>).*', r'\1',
                          tab_html, flags=re.DOTALL)
    else:
        tab_html = "Parsing was not successful"
    (ans, align, tab_st, rapp)  = answer_to_fine_list(langpro_answer)
    return { 'tableau':tab_html,
             'answer':ans,
             'align':align,
             'status':tab_st,
             'apps':rapp }

######################
# replace _G variables with X variables
def pretty_G_variables(proof):
    #print '<pre>{}</pre>'.format(proof)
    orig_proof = proof
    proof = re.sub(' *@ *', '@', proof)
    #print '*****lines in proof {}*****'.format(len(proof))
    proof = re.sub('(_G\d+),', r'\1.', proof)
    #print '*****lines in proof {}*****'.format(len(proof))
    g_vars = re.findall('_\d+', proof)
    #print '*****gvars in proof {}*****'.format(len(g_vars))
    replace = {}
    counter = 0
    for var in g_vars:
        if var in replace:
            pass
        else:
            counter += 1
            replace[var] = str(counter)
    if replace:
        g_pattern = '({})'.format('|'.join(replace.keys()))
        #print '*****{}*****'.format(g_pattern)
        proof = re.sub(g_pattern, (lambda x: replace[x.group(0)]), proof)
    return proof

######################
def answer_to_fine_list(answer):
    #yes_al_closed11, no_na_open_Ter15
    m = re.search('([a-z]+)_([a-z]+)_([A-Za-z_]+)(\d+)', answer)
    if not m:
        return ('NA', 'NA', 'NA', 'NA')
    else:
        (ans, align, stat, rapp) = m.groups()
        # get entailment answers and tableau status
        #print '<xmp>{}</xmp>'.format(stat)
        if re.search('closed', stat):
            ans = 'ENTAILMENT' if re.search('yes', ans) else 'CONTRADICTION'
            status = 'closed'
        else:
            ans = 'NON-ENTAILMENT' if re.search('yes', ans) else 'NON-CONTRADICTION'
            status = 'limited' if re.search('lim', stat, re.I) else 'terminated'
        # get alignment status
        align = 'Aligned' if re.search('al', align) else 'Non-aligned'
        #status = '{}({})'.format(status, rapp)
        return ans, align, status, rapp


######################
def aggregate_answers(ent, cont):
    aggr = '{} {}'.format(ent, cont)
    if re.search('non-entailment contradiction', aggr, re.I):
        return "CONTRADICTION"
    elif re.search('non-entailment non-contradiction', aggr, re.I):
        return "NEUTRAL"
    elif re.search('entailment non-contradiction', aggr, re.I):
        return "ENTAILMENT"
    elif re.search('(contra.+entail|entail.+contra)', aggr, re.I):
        return "NEUTRAL (prob. inconsistent premises)"
    elif re.search('entailment', aggr, re.I):
        return "ENTAILMENT"
    elif re.search('contradiction', aggr, re.I):
        return "CONTRADICTION"
    elif re.search('neutral', aggr, re.I):
        return "NEUTRAL"
    else:
        return "UNEXPECTED OUTCOME"

######################
def aggregate_answers(answers):
    '''combine a list of answers in one answer
    '''
    if 'ENTAILMENT' in answers:
        if 'CONTRADICTION' in answers:
            return "NEUTRAL (inconsistent predictions)"
        else: # Contradiction not in answers
            return "ENTAILMENT"
    else: # 'Entailment' not in answers
        if 'CONTRADICTION' in answers:
            return 'CONTRADICTION'
        else:
            return "NEUTRAL"

#######################
def user_input_to_pl_spl(problem):
    '''Return a prolog representation of the problem
       and sentence per line format as strings
    '''
    try:
        [prems, hypo] = re.split(r'\s*\n\s*[-]+\s*\n\s*', problem)
    except:
        return '', ''
    #print '<xmp>{}\n{}</xmp>'.format(prems, hypo)
    #print '<xmp>{}</xmp>'.format(re.split(r'\s*\n\s*', prems))
    sen_list = re.split(r'\s*\n\s*', prems)
    sen_list += [hypo]
    sen_pl = spl = ''
    #print '<xmp>{}</xmp>'.format(sen_list)
    for i, s in enumerate(sen_list):
        s = sent_preprocess(s)
        tok = ' '.join(nltk.word_tokenize(s))
        tok_esc = tok.replace("'", "\\'")
        status = 'h' if (i == len(sen_list) - 1) else 'p'
        sen_pl += "sen_id({0}, 1, '{1}', 'nil', '{2}').\n".format(i+1, status, tok_esc)
        spl += '\n' + tok_esc
    return sen_pl, spl

#########################
def sent_preprocess(sen):
    return sen

#########################
def ccg_parsing(parser, sen, v=0):
    '''parse the sentence in prolog format
       with a specified ccg parser
    '''
    if parser == 'easyccg':
        return easyccg_parsing(sen, v=v)
    elif parser == 'cc':
        # append newline to make sure the last sentence is parsed
        return cc_parsing(sen + '\n', v=v)
    elif parser == 're-cc':
        # append newline to make sure the last sentence is parsed
        return re_cc_parsing(sen + '\n', v=v)
    else:
        raise RuntimeError('Unknown parser: {}').format(parser)

#########################
def cc_parsing(sen, v=0):
    '''parse with C&C with non-rebanked model
    '''
    sen_esc = sen.replace('"', '\\"')
    path = 'parsers/candc'
    cmd = ('{0}/candc/bin/candc  --models {0}/models/models '
           '--candc-printer boxer  --candc-parser-noisy_rules=false'
           ).format(path)
    if v:
        print(f"CCG parsing command:\n{cmd}")
    return run_tool(cmd, sen_esc)

#########################
def re_cc_parsing(sen, v=0):
    '''parse with C&C with a rebanked model
    '''
    sen_esc = sen.replace('"', '\\"')
    path = 'parsers/rebank_candc'
    cmd = ('{0}/rebank_dist/bin/candc  --models {0}/models '
           '--candc-super {0}/super  --candc-parser {0}/model_hybrid '
           '--candc-printer boxer  --candc-parser-noisy_rules=false'
           ).format(path)
    if v:
        print(f"rebanked CCG parsing command:\n{cmd}")
    return run_tool(cmd, sen_esc)

#########################
def easyccg_parsing(sen, v=0):
    '''parse with EasyCCG with non-rebanked model
    '''
    cc_bin = 'parsers/rebank_candc/rebank_dist/bin'
    cc_models = 'parsers/rebank_candc/models'
    pos_ner = ('{0}/pos --model {1}/pos | {0}/ner --model {1}/ner '
               '-ofmt "%w|%p|%n \\n"').format(cc_bin, cc_models)
    easy_model = 'parsers/models_easyccg/standard'
    easy_jar = 'parsers/easyccg/easyccg.jar'
    easy_java = 'java -jar {0} --model {1} -i POSandNERtagged -o prolog'.format(
                easy_jar, easy_model)
    perl = 'perl EasyCCG/prolog_to_boxer.perl'
    prolog_to_boxer = 'EasyCCG/prologCCG_to_boxerCCG.pl'
    sen_esc = sen.replace('"', '\\"')
    cmd = 'echo "{0}" | {1} | {2} | {3}'.format(
          sen_esc, pos_ner, easy_java, perl)
    if v:
        print(f"EasyCCG parsing command:\n{cmd}")
    out = run_tool(cmd)
    assert_cl = assertz_clause(out)
    cmd = 'swipl -f {0} -g "{1}, prolog_to_boxer_stdout, halt"'.format(
          prolog_to_boxer, assert_cl)
    if v:
        print(f"swipl conversion command:\n{cmd}")
    out = run_tool(cmd)
    return out

#########################
def assertz_clause(pl):
    '''Given a prolog code, convert it to
       a code that asserts the facts inside it
    '''
    clauses = re.findall('((?:sen_id|ccg|w)\(.+?\))\.', pl, re.DOTALL)
    assertz = [ 'assertz({})'.format(cl) for cl in clauses ]
    return ',\n\n'.join(assertz)


#########################
def security_clean(string):
    '''Leave only alphanumeric characters, dashes, underscores, and periods
       + comma
    '''
    if string is None:
        return None
    if type(string) is list:
        return [ security_clean(x) for x in string ]
    else:
        #print "<xmp>before\n{}</xmp>".format(string)
        out = re.sub('[^\w0-9_\s\-.,]', '', string, flags=re.UNICODE)
        #print "<xmp>after\n{}</xmp>".format(out)
        return out


#########################
def tableau_info(al, status, apps, kb):
    #print "<xmp>terlimN = {}</xmp>".format(terlimN)
    #print "<xmp>kb = {}</xmp>".format(kb)
    kb = 'empty' if kb == '' \
                 else re.sub('(\w+)\(', r'<span class="kb_predicate">\1</span>(', kb)
    info = (' <div class="tableau_info">The tableau uses <b>{al}</b> LLFs and'
            ' it is <b>{status}</b> after <b>{apps}</b> rule applications.'
            ' The used KB is <span class="tab_kb">{kb}</span>.</div>'
           ).format(**locals())
    return info

#########################
# def log_visit

#########################
# def readable_ip
