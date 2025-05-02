<?php
echo <<<PRINT
	<form id="contact_form" action="report.cgi" method="get" class="contact">
	    <!--<div style="color:white; font-weight:bold; margin-bottom:5px;">Contact &amp; Report Form</div> -->
	    <input name="contact_name" placeholder="Name" class="contact_field"/>
	    <input name="contact_email" placeholder="Email" class="contact_field"/>
	    <div style="color:black; font-weight:bold;">Message</div> 
	    <textarea id="message_text" name="message" rows="3" data-min-rows='3' placeholder="Type a message here..." class="contact_field"></textarea>
	    <div style="text-align:right">
	    	<span id="message_status" style="color:red; font-weight:bold;"></span>
	        <button id="send_button" type="button" class="send_btn" onclick="send_message()">SEND</button>
	  	</div>
	    <!--<input type="submit"  style="border: solid 1px black;" value="send">-->
	</form>
PRINT;
?>
