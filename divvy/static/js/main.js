/* main application for divvy */
define(['global', 'jquery', 'jquery-mobile', 'knockout'], function(global, $, $m, ko){
    // flask api urls
    var
        tags_url = $('#api-tags').val()
        , buckets_url = $('#api-buckets').val()
    ;

    // bucket definition
    var Bucket = function(){
        return {
            'id': null
            , 'description': ko.observable()
            , 'schedule': ko.observable()
            , 'sources': ko.observableArray([])
        };
    };

    var buckets;

    // when the 'content' panel is opened, focus on the search filter
    $('#content').bind('panelopen', function(){
        $('#content input[data-type="search"]').focus();
    });

    // pull tags and their sources
    $.get(tags_url, null, function(data){
        ko.applyBindings(data, $('#content')[0]);
        $('#content').trigger('create');
    }, 'json');

    // pull buckets and their sources
    $.get(buckets_url, null, function(data){
        var new_buckets = [];

        for(var i = 0; i < data.length; i++){
            var bucket = Bucket();
            bucket.id = data[i].id;
            bucket.description(data[i].description);
            bucket.schedule(data[i].schedule);
            bucket.sources(data[i].sources);
            new_buckets.push(bucket);
        }

        buckets = ko.observableArray(new_buckets);

        ko.applyBindings(buckets, $('#buckets')[0]);
        $('#buckets').trigger('create');
    }, 'json');
});
