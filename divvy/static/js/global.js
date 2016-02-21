define(['jquery', 'jquery-mobile'], function($, $m){
	var t;

	$(window).bind('resize', function(){
		clearTimeout(t);
		t = setTimeout(function(){
			$(document).trigger('updatelayout');
			$('.ui-panel').height($('.ui-page').height());
		}, 100);
	});

	$(document).bind('pageshow', function(){
		$(window).trigger('resize');
	});
});
