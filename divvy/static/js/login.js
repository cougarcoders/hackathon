define(['global', 'jquery', 'jquery-mobile'], function(global, $, $m){
	$(document).bind('pageinit pageshow', '#login-page', function(e) {
		$('#username').focus();
	});
});
