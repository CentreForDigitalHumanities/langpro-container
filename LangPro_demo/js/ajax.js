function prove(b) {
	var xmlhttp;
	//document.getElementById("status").style.display = "inline";
	if (window.XMLHttpRequest){
		// code for IE7+, Firefox, Chrome, Opera, Safari
  		xmlhttp=new XMLHttpRequest();
  	}
	else{// code for IE6, IE5
  		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  	}
	
	//var block = 'Processing Request... <img style="width:10%;" src="img/tree_grow.gif"/>';

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200){ 
			$("body").removeClass("loading"); 
			document.getElementById("proof").innerHTML=xmlhttp.responseText;
            document.getElementById("status").innerHTML=""; }
		else if (xmlhttp.readyState==0) { 
			$("body").addClass("loading");
			document.getElementById("status").innerHTML="Request not initialized"; }
		else if (xmlhttp.readyState==1) { 
			$("body").addClass("loading");
			document.getElementById("status").innerHTML="Parsing &amp; proof procedures may take some time"; }
		else if (xmlhttp.readyState==2) { 
			$("body").addClass("loading");
			console.log($(form).attr("action") + "?" + $(form).serialize())
			document.getElementById("status").innerHTML="Request Received"; }
		else if (xmlhttp.readyState==3){ 
			//document.getElementById("proof").innerHTML='Processing Request... <img style="width:10%;" src="img/tree_grow_r.gif"/>'; }
			//$.blockUI({message: 'sdadsdsdsfsdf' }); }
			$("body").addClass("loading"); }
			//document.getElementById("modal").show(); }
		//else 
			//{ document.getElementById("LLF").innerHTML="Something else happening";	}
	}
	//alert(b);
	var form = $(b).closest("form"); //wrap in jQuery if Jquery method is going to be used
	//alert(form);
	//alert($(form).attr("action"));
	//alert($(form).serialize());
	var url = $(form).attr("action") + "?" + $(form).serialize();
	//alert(url);
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
	//document.getElementById("status").style.display = "none";
	document.getElementById("proof").style.display = "block";

//	loadjscssfile("css/ttterms.css", "css") 
//	loadjscssfile("js/my.js", "js") 
//	loadjscssfile("js/myfunction.js", "js") 
//	loadjscssfile("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.min.css", "css") 

	//tableau_acl.cgi?sick_set=trial&chk=prprb&chk=prlim&chk=wn_ant&limit=50&userinput=1-20
	//tableau_acl.cgi?sick_set=trial&chk=prprb&chk=prlim&chk=wn_ant&limit=50&button=Prove&userinput=1-20
	//document.getElementById("proof").innerHTML= url;
}




function send_message() {
	var xmlhttp;
	//document.getElementById("status").style.display = "inline";
	if (window.XMLHttpRequest){
		// code for IE7+, Firefox, Chrome, Opera, Safari
  		xmlhttp=new XMLHttpRequest();
  	}
	else{// code for IE6, IE5
  		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  	}
	
	//var block = 'Processing Request... <img style="width:10%;" src="img/tree_grow.gif"/>';

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200){ 
			$("body").removeClass("loading"); 
			document.getElementById("message_status").innerHTML=xmlhttp.responseText;
            document.getElementById("status").innerHTML=""; }
		else if (xmlhttp.readyState==0) { 
			$("body").addClass("loading");
			document.getElementById("status").innerHTML="Request not initialized"; }
		else if (xmlhttp.readyState==1) { 
			$("body").addClass("loading");
			document.getElementById("status").innerHTML="Server Connection established"; }
		else if (xmlhttp.readyState==2) { 
			$("body").addClass("loading");
			document.getElementById("status").innerHTML="Request Received"; }
		else if (xmlhttp.readyState==3){ 
			//document.getElementById("proof").innerHTML='Processing Request... <img style="width:10%;" src="img/tree_grow_r.gif"/>'; }
			//$.blockUI({message: 'sdadsdsdsfsdf' }); }
			$("body").addClass("loading"); }
			//document.getElementById("modal").show(); }
		//else 
			//{ document.getElementById("LLF").innerHTML="Something else happening";	}
	}
	var url = $("#contact_form").attr("action") + "?" + $("#contact_form").serialize();
	//alert(url);
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
	alert("Message was successfully sent");
	//document.getElementById("message_status").style.display = "none";
	//document.getElementById("send_button").style.display = "none";
	//tableau_acl.cgi?sick_set=trial&chk=prprb&chk=prlim&chk=wn_ant&limit=50&userinput=1-20
	//tableau_acl.cgi?sick_set=trial&chk=prprb&chk=prlim&chk=wn_ant&limit=50&button=Prove&userinput=1-20
}




function loadjscssfile(filename, filetype){
    if (filetype=="js"){ //if filename is a external JavaScript file
        var fileref=document.createElement('script')
        fileref.setAttribute("type","text/javascript")
        fileref.setAttribute("src", filename)
    }
    else if (filetype=="css"){ //if filename is an external CSS file
        var fileref=document.createElement("link")
        fileref.setAttribute("rel", "stylesheet")
        fileref.setAttribute("type", "text/css")
        fileref.setAttribute("href", filename)
    }
    if (typeof fileref!="undefined")
        document.getElementsByTagName("head")[0].appendChild(fileref)
}
 


//not used
function valthis() {
var checkBoxes = document.getElementsByClassName('parser_chkbx');
var isChecked = false;
    for (var i = 0; i < checkBoxes.length; i++) {
        if ( checkBoxes[i].checked ) {
            isChecked = true;
        };
    };
    if ( isChecked ) {
        alert( 'At least one checkbox checked!' );
        } else {
            alert( 'Please, check at least one checkbox!' );
        }   
}





