define(['jquery', 'jquery-mobile'], function($, $m){
	var t;

	$(window).bind('resize', function(){
		clearTimeout(t);
		t = setTimeout(function(){
			$('.ui-panel').css('min-height', $('.ui-page').height() + 'px');
		}, 10);
	});

	$(document).bind('pageshow', function(){
		$(window).trigger('resize');
	});
});
