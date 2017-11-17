$(document).ready(function () {
	var url = window.location.href;
	var user_id = url.split('/')[4].split('?')[0];	
	var mode = url.split('=')[1];

	var dark = false;
    var c = document.cookie.split(" ");
    for (var i = 0; i < c.length; i++)
        if (c[i].startsWith("cflags"))
            dark = c[i].split("=")[1].startsWith("1")

	var std = 'hidden'; 
	var taiko = 'hidden';
	var ctb = 'hidden';
	var mania = 'hidden';
	
	if (mode === "0"){
		std = '';
	}else if(mode === "1"){
		taiko = '';
	}else if(mode === "2"){
		ctb = '';
	} else if(mode === "3"){
		mania = '';
	}
	
	$("<div class='ui raised segment twemoji' id='userpage-content' data-mode='0' " + std + "><iframe frameBorder='0' scrolling='no' width='100%' height='400px' src='http://127.0.0.1:7001/" + user_id + "/0/" + dark + "/'></iframe></div>").insertAfter( "#mode-menu" );
	
	$("<div class='ui raised segment twemoji' id='userpage-content' data-mode='1' " + taiko + "><iframe frameBorder='0' scrolling='no' width='100%' height='400px' src='http://127.0.0.1:7001/" + user_id + "/1/" + dark + "/'></iframe></div>").insertAfter( "#mode-menu" );
	
	$("<div class='ui raised segment twemoji' id='userpage-content' data-mode='2' " + ctb + "><iframe frameBorder='0' scrolling='no' width='100%' height='400px' src='http://127.0.0.1:7001/" + user_id + "/2/" + dark + "/'></iframe></div>").insertAfter( "#mode-menu" );
	
	$("<div class='ui raised segment twemoji' id='userpage-content' data-mode='3' " + mania + "><iframe frameBorder='0' scrolling='no' width='100%' height='400px' src='http://127.0.0.1:7001/" + user_id + "/3/" + dark + "/'></iframe></div>").insertAfter( "#mode-menu" );
});