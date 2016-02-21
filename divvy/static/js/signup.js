/* sign-up for divvy */
define(['global', 'jquery', 'jquery-mobile'], function(global, $, $m){
    // focus on the username field when the page is shown
	$(document).bind('pageshow', '#signup-page', function() {
		$('#username').focus();
	});
});
