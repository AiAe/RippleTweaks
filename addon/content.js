$(document).ready(function () {
	var url = window.location.href;
	var user_id = url.split('/')[4].split('?')[0];
	var mode = url.split('=')[1];

	$( "<iframe frameBorder='0' scrolling='no' width='100%' height='400px' src='http://127.0.0.1:7001/" + user_id + "/" + mode + "/'></iframe>" ).insertAfter( "#mode-menu" );
});