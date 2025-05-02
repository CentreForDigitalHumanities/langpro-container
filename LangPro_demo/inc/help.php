<?php
echo <<<PRINT
<div class="help_block">
LangPro produces Lambda Logical Forms (LLFs) from CCG derivations.
The CCG derivations are produced by the C&amp;C and EasyCCG parsers.
You can choose both parsers and LangPro will consider LLFs based on the derivations from each parser.
Do not forget to choose at least one parser.
</div>

<div class="help_block">
For each argument, LangPro automatically generates a knowledge base from WordNet.
</div>

<div class="help_block">
The tab for the SICK problems loads slowly as it contains 4.5K problems.
Processing a user input takes more time as parsers are loaded to parse the input.
</div>

<div class="help_block">
There are two types of open tableaux.  
If no rule application can be carried out on its open branches, an open tableau is <b>terminated</b>,
otherwise it is <b>limited</b>, i.e. the rule application limit is reached and it forbids further rule applications. 
</div>

<div class="help_block">
The intuition behind tableau nodes:

<div style="text-align: center; margin-top: 7px;">
<div class="node">
<span class="node_id">node id</span><span class="formula true">
<span class="modList">list of modifiers</span>
<span class="llf">head term of a <b>true</b> node</span>
<span class="argList">list of arguments</span>
</span>
</div>
<div class="source" style="margin-bottom:15px">
<span class="source">rule id [a list of nodes it applies to]</span></div>
</div>

<div style="text-align: center">
<div class="node">
<span class="node_id">node id</span><span class="formula false">
<span class="modList">list of modifiers</span>
<span class="llf">head term of a <b>false</b> node</span>
<span class="argList">list of arguments</span>
</span>
</div>
<div class="source"><span class="source">i.e. a rule application that triggers the node</span></div>
</div>

</div>


PRINT;
?>
