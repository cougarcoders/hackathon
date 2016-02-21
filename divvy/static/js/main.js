define(['jquery', 'jquery-mobile'], function($, $m){
	$.mobile.loading('show');

	$('#content').bind('panelopen', function(){
		$('#content input[data-type="search"]').focus();
	});

	$('[data-role="page"]').bind('pageshow', function() {
		$.mobile.loading('hide');
	});
});
