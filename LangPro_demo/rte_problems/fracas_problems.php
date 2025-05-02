<?php

//ini_set('display_errors', 1);
//ini_set('display_startup_errors', 1);
//error_reporting(E_ALL);

$text = file_get_contents('rte_problems/myfracas.html');
//preg_match('~<div id="fracas_problems_style".+</div>~s', $text, $matches);
$text = preg_replace('~^.+?(<div class="rte_problems_style".+</div>).*$~s', '$1', $text);

//$regex = '#(<table class="tb_id_answer">.+?fracas-0*(\d+).+?)(</tr>\s*</table>)#s';
//$replacement ='$1<td><button class="libtn" type="button" onclick="prove()">PROVE</button></td>$3';

$regex = '#(<table class="tb_prob">\s*<tr>(\s*))(<td .+?fracas-0*(\d+).+?</tr>\s*)</table>\s*<table[^<]*#s';
$replacement ='$1<td width="7%"><input type="radio" name="prob_id" value="$4"></td>$2$3  ';

$text = preg_replace($regex, $replacement, $text);

echo $text;

?>