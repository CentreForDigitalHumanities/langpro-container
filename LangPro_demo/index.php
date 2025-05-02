<?php
# Uncomment for debugging
# ini_set('display_errors', 'On');
# error_reporting(E_ALL);
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
		<title>LangPro</title>

		<!--SCRIPTS and CSS-->
		<?php include 'inc/style_script.php'; ?>
	</head>

	<!--##############  BODY #################-->
	<body>
		<div id="github_link"><a href="https://github.com/kovvalsky/LangPro"><img width="50px" src="img/github.png"></img></a></div>
		<div style="display:table; width: 100%;">
			<div class="main">
				<div style="font-weight: bold; font-size:140%; text-align: center; padding-bottom: 10px;">
					<span class="seablue" style="font-size:140%;">LangPro</span>
					<span>: Natural <span class="seablue">Lang</span>uage Theorem <span class="seablue">Pro</span>ver</span>
				</div>
				<div>LangPro tries to find out a semantic relation between
				a <span class="key_bg_lbl">set of premises</span> and a <span class="key_bg_lbl">hypothesis</span>.
				The semantic relation can be:
					<span title="Whenever all premises hold, the hypothesis holds too"><span class=key_bg_vio>entailment</span>/<span class=key_bg_vio>yes</span></span>,
					<span title="Whenever  all premises hold, the conclusion does not hold"><span class=key_bg_vio>contradiction</span>/<span class=key_bg_vio>no</span></span>,
					<span title="None of the two previous cases, i.e. non-entailment &amp; non-contradiction"><span class=key_bg_vio>neutral</span>/<span class=key_bg_vio>unknown</span></span>.
					<br/>
					LangPro obtains competetive results on the <a href="http://clic.cimec.unitn.it/composes/sick.html">SICK</a> and <a href="https://nlp.stanford.edu/~wcmac/downloads/fracas.xml">FraCaS</a> RTE
					(i.e. recognizing textual entailment) datasets.
					<br/>
					The version used for the demo is outdated. Consult the <a href="https://github.com/kovvalsky/LangPro">GitHub</a> repo for the recent version of LangPro.
					<br/>
					<strong>The inputs to the prover are recorded</strong>
				</div>
				<!--################ Form ###################-->
				<!--################ TABS ###################-->
				<div style="width: 1000px;">
					<div class="tabs">
						<ul class="tab-links">
							<li class="active"><a href="#tab_user_input">User input</a></li>
							<li><a href="#tab_sick_problems">SICK problems</a></li>
							<li><a href="#tab_fracas_problems">FraCaS problems</a></li>
							<li><a href="#tab_help">Help</a></li>
							<li><a href="#tab_references">References</a></li>
							<li><a href="#tab_report_contact">Report/Contact</a></li>
						</ul>
						<!--<div style="display:block">
							<select id="data_type" name="data_type">
								<option value="tab_user_input" selected="selected">user input</option>
								<option value="tab_sick_problems">sick</option>
								<option value="tab_fracas_problems">fracas</option>
							</select>
						</div>-->
						<div class="tab-content">
							<!--##### USER INPUT #####-->
							<div id="tab_user_input" class="tab active">
								<form id="user_input_form" action="/api/user/" method="get">
									<input name="data_type" value="user_input" style="display:none" />
									<div style="display:block; padding:10px; margin-top:10px; border: 1px solid gray;">
										<div style="margin:-22px 0px 10px 0px;">
											<span style="background:white; padding:0px 5px">Type a natural language
												argument (i.e. premises and a concusion) and format it as the example
												below</span>
										</div>
										<textarea id="argument" data-min-rows="4" rows="4" type="text"
											name="rte_problem" style="width:99.3%; font-size: 120%" class="autoExpand"
											>Every man is working
Everybody who is working has an expensive car
---
Every man owns a car</textarea>
									</div>
									<?php include 'inc/proof_config.php'; ?>
								</form>
							</div>
							<!--##### SICK Problems #####-->
							<div id="tab_sick_problems" class="tab">
								<form id="sick_problems_form" action="/api/sick/" method="get">
									<input name="data_type" value="sick_problems" style="display:none" />
									<div style="height:400px; overflow-y: auto; overflow-x: auto;">
										<div style="padding: 7px 0px;">Choose a problem below and prove it. The problems
											are drawn from the training portion of SICK (4500 problems).<br/>
											The sentences are parsed beforehand by both parsers. This significantly decreases the processing time.</div>
										<?php include 'rte_problems/sick_train.php'; ?>
									</div>
									<?php include 'inc/proof_config.php'; ?>
								</form>
							</div>
							<!--##### FraCaS Problems #####-->
							<div id="tab_fracas_problems" class="tab">
								<form id="fracas_problems_form" action="/api/fracas/" method="get">
									<input name="data_type" value="fracas_problems" style="display:none" />
									<div style="height:400px; overflow-y: auto; overflow-x: auto;">
										<div style="padding: 7px 0px;">Choose a problem below and prove it. LangPro is
											adapted to the phenomena found in Sections 1, 2, 5, 9.<br/>
											The sentences are parsed beforehand by both parsers. This significantly decreases the processing time.</div>
										<?php include 'rte_problems/fracas_problems.php'; ?>
									</div>
									<?php include 'inc/proof_config.php'; ?>
								</form>
							</div>
							<!--##### References #####-->
							<div id="tab_help" class="tab">
								<?php include 'inc/help.php'; ?>
							</div>
							<!--##### References #####-->
							<div id="tab_references" class="tab">
								<?php include 'inc/references.php'; ?>
							</div>
							<!---CONTACT-->
							<div id="tab_report_contact" class="tab">
								<?php include 'inc/report_contact.php'; ?>
							</div>
						</div>
					</div>
				</div>
				<p id="demo"></p>
				<!---
<h4 id="ref" onclick="toggle_block('listRefs')"><a href="#">References</a></h4>
<div id="listRefs" style="display:none">Hide this text</div>
-->
				<div id="status"></div>
			</div>
		</div>
		<div id="proof" class="secondary" style="display:block;">
			<!--<div class="tabs">
				<span>Tableaux built to verify the argument on <b>Relation</b> while using the derivations
					from <b>Parser</b>
				</span>
				<ul class="tab-links">
					<li><a href="#tab_cc_ent">Entailment &amp; C&amp;C</a></li>
					<li><a href="#tab_cc_cont">Contradiction &amp; C&amp;C</a></li>
					<li><a href="#tab_easy_ent"> Entailment &amp; EasyCCG</a></li>
					<li><a href="#tab_easy_cont">Contradiction &amp; EasyCCG</a></li>
				</ul>
				<div class="tab-content">
					<div id="tab_cc_ent" class="tab">
						<p>Clickable SICK dataset</p>
					</div>
					<div id="tab_cc_cont" class="tab">
						<p>Clickable FraCaS dataset</p>
					</div>
					<div id="tab_easy_ent" class="tab"> </div>
					<div id="tab_easy_cont" class="tab"> </div>
				</div>
			</div>-->
		</div>
		<div class="modal"><!-- Place at bottom of page --></div>
	</body>
</html>
