define(['jquery', 'jquery-mobile'], function($, $m){
	var t;

	$(window).bind('resize', function(){
		clearTimeout(t);
		t = setTimeout(function(){
			$('.ui-panel').height($('.ui-page').height());
		}, 10);
	});

	$(document).bind('pageshow', function(){
		$(window).trigger('resize');
	});
});
