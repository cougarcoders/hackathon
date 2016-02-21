define(['global', 'jquery', 'jquery-mobile'], function(global, $, $m){
	$(document).bind('pageinit pageshow', '#signup-page', function() {
		$('#username').focus();
	});
});
