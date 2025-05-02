<?php
echo <<<PRINT
  <div class="proof_config">
    <span style="float:left; padding-top:4px;">
  	<input type ="checkbox" class="prover_par" name="parser" value = "cc" checked="checked" title="Use the rebanked C&amp;C parser to get CCG derivations"/>C&amp;C&nbsp;
  		<input type ="checkbox" class="prover_par" name="parser" value = "easyccg" checked="checked" title="Use the EasyCCG parser to get CCG derivations"/>EasyCCG&nbsp;
  			<input type ="checkbox" class="prover_par" name="prover_config" value = "allInt" checked="checked" title="Treat noun modifiers as intersective by default, e.g. a baby elephant is a baby and an elephant"/>interDef&nbsp;
  				<input type ="checkbox" class="prover_par" name="prover_config" value = "aall" checked="checked" title="Allow alignment of any non-downward monotone terms, e.g. a~dog"/>alignAll&nbsp;
  	<!--<input type="number" name="ral" min="0" max="1000" value="400">max rule apps&nbsp;</input>-->
  				&nbsp;&nbsp;max rule app <input class="prover_par" name="ral" type="text" size="3" value="200"/>&nbsp;&nbsp;
  	first <select id="senses" name="senses" class="prover_par">
  		<option value="all" selected="selected">all</option>
  		<option value="1">1</option><option value="2">2</option><option value="3">3</option>
  		<option value="4">4</option><option value="5">5</option><option value="6">6</option>
  		<option value="7">7</option><option value="8">8</option><option value="9">9</option>
  		<option value="10">10</option><option value="15">15</option><option value="20">20</option>
  	</select> senses per word&nbsp;
  	</span>
  	<button class="btn" type="button" onclick="prove(this)">PROVE</button>
  </div>  
PRINT;
?>
