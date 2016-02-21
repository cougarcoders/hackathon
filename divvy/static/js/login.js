define(['jquery', 'jquery-mobile'], function($, $m){
	$('[data-role="page"]').bind('pageshow', function(e) {
		$('#username').focus();
	});
});
