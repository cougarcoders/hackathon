define(['jquery', 'jquery-mobile'], function($, $m){
	$.mobile.loading('show');

	$('[data-role="page"]').bind('pageshow', function(e) {
		$.mobile.loading('hide');
		$('#username').focus();
	});
});
