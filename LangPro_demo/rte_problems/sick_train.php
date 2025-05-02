<?php
  
$text = file_get_contents('rte_problems/SICK_train.txt');
//preg_match('~<div id="fracas_problems_style".+</div>~s', $text, $matches);
$text = preg_replace('#^.+?(\d)#s', '$1', $text);



//$regex = '#(\d+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([A-Z]+)#';
//preg_match_all($regex, $text, $matches);
//print_r($matches);

$regex = '#(\d+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([A-Z]+)#';

$replacement = <<<HEREDOC
<div class="problem">
    <table class="tb_prob">
      <tr>
        <td width="7%"><input type="radio" name="prob_id" value="$1"></td>
        <td class="prob-id">sick-$1</td>
        <td class="prob-ans">answer: <span class="ans_color_$5">$5</span></td>
        <td class="relatedness">relatedness score: <span class="rel_score">$4</span></td>
      </tr>
      <tr>
        <td>P</td>
        <td colspan="3">$2</td>
      </tr>
      <tr>
        <td>H</td>
        <td colspan="3">$3</td>
      </tr>
    </table>
</div>\n
HEREDOC;

$text = preg_replace($regex, $replacement, $text);
echo '<span class="rte_problems_style">' . $text . '<\span>';

?>
