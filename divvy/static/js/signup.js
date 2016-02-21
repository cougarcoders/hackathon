define(['global', 'jquery', 'jquery-mobile'], function(global, $, $m){
	$(document).bind('pageshow', function(e) {
		$('#username').focus();
	});
});
