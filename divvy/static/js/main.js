define(['global', 'jquery', 'jquery-mobile', 'knockout'], function(global, $, $m, ko){
	var tags_url = $('#api-tags').val();

	$('#content').bind('panelopen', function(){
		$('#content input[data-type="search"]').focus();
	});

	$.get(tags_url, null, function(data){
		ko.applyBindings(data, $('#content')[0]);
        $('#content').trigger('create');
	}, 'json');
});
