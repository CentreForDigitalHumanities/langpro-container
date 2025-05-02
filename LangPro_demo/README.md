# LangPro Online Demo

A description of the demo directory and environment.

## Directory

* `xslt_junk/` - generated xml files are written here to be rendered later on the frontend.
* `rte_problems/` - contains existing NLI datasets, namely, FraCaS and SICK are used by the demo. The used files are ones with `*_sen_(d_)?.?_ccg.pl` names. ccg, eccg, occg, reccg are names of variations of CCG parsers.
* `inc/` - a collection of php parts included in other php files.

* `nat_lang_pro/langpro` - a binary that is doing proving. 
When proving let's say the 5th problem from SICK then, it runs as:

  ```bash
  swipl -x nat_lang_pro/langpro  -g " parList([proof_tree, pr_kb, effCr([equi, nonBr, nonProd, nonCons]), wn_ant, wn_der, wn_sim, ral(200),  allInt, aall]), online_demo(5), halt" -l rte_problems/SICK_train_sen_ccg.pl 
  ```
  
  When proving problems from the user input, e.g., P=`A dog runs` & H=`An animal runs`, it runs as:

  ```bash
  swipl -x nat_lang_pro/langpro  -g "assertz(sen_id(1, 1, 'p', 'nil', 'A dog runs')), assertz(sen_id(2, 1, 'h', 'nil', 'An animal runs')), assertz(ccg(1,ba(s:dcl,fa(np,t(np/n, 'A', 'a', 'DT', 'I-NP', 'O'),t(n, 'dog', 'dog', 'NN', 'I-NP', 'O')),t(s:dcl\np, 'runs', 'run', 'VBZ', 'I-VP', 'O')))), assertz(ccg(2, ba(s:dcl, fa(np, t(np/n, 'An', 'an', 'DT', 'I-NP', 'O'), t(n, 'animal', 'animal', 'NN', 'I-NP', 'O')), t(s:dcl\np, 'runs', 'run', 'VBZ', 'I-VP', 'O')))),  parList([proof_tree, pr_kb, effCr([equi, nonBr, nonProd, nonCons]), wn_ant, wn_der, wn_sim, ral(200),  allInt, aall]), online_demo(1), halt" 
  ```

  In both cases, output contains xml elements:

  ```xml
  <parsed_problem>
    <parsed_sentence>
      <ccg_tree> <ccg_term> <corr_ccgterm> <llf>
    <parsed_sentence>
      <ccg_tree> <ccg_term> <corr_ccgterm> <llf>
  <tableau>
  <tableau>
  ```

* `EasyCCG/` - contains scripts that post-process the output derivations from EasyCCG.
* `parsers/` - contains two parsers, EasyCCG and (rebanked) C&C
  * Working C&C parser can be tested with this command:
  
    ```bash
    echo "A cat is sleeping" | parsers/rebank_candc/rebank_dist/bin/candc --models parsers/rebank_candc/models --candc-super parsers/rebank_candc/super --candc-parser parsers/rebank_candc/model_hybrid --candc-printer boxer --candc-parser-noisy_rules=false
    ```

  * Working EasyCCG parser can be tested with this command:

    ```bash
    echo "A cat is jumping" | parsers/rebank_candc/rebank_dist/bin/pos --model parsers/rebank_candc/models/pos | parsers/rebank_candc/rebank_dist/bin/ner --model parsers/rebank_candc/models/ner -ofmt "%w|%p|%n \n" | java -jar parsers/easyccg/easyccg.jar --model parsers/models_easyccg/standard -i POSandNERtagged -o prolog
    ```

  * `LP_git` - clone of LangPro repo. It seems that binary `nat_lang_pro/langpro` is compiled in 2019 and it is not clear which version of LangPro sources were used. There is a need to adapt the current LangPro repo to the demo, but meantime the binary can be used.

* `run_langpro.cgi` - defines required paths in `kw` dictionary.

## Required tools

What needs to be installed (versions are not hard constraint, just a hint what is currently on the server):

```
xsltproc (Using libxml 20903, libxslt 10128 and libexslt 817)
swipl (8.0.1)
perl (v5.22.1)
python 2.7
```