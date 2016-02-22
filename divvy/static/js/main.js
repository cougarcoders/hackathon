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

    // viewmodels and helper variables
    var
        buckets = {
            'content': null
            , 'remove_from_bucket_popup': function(source, bucket){
                buckets.target_bucket = bucket;
                buckets.target_source = source;
                return true;
            }
            , 'remove_from_bucket': function(){
                $.ajax({
                    url: buckets_url + '/' + buckets.target_bucket.id + '/' + buckets.target_source.id
                    , type: 'DELETE'
                    , dataType: 'json'
                    , success: function(data){
                        if(data.hasOwnProperty('errors')) {
                            data.errors.forEach(function(val, idx, arr){
                                console.log(val);
                            });
                        }
                        else {
                            buckets.target_bucket.sources.splice(buckets.target_bucket.sources.indexOf(buckets.target_source), 1);
                        }
                    }
                });

                return true;
            }
            , 'add_to_bucket': function(){
                $.ajax({
                    url: buckets_url + '/' + buckets.target_bucket.id + '/' + buckets.target_source.id
                    , type: 'PUT'
                    , dataType: 'json'
                    , success: function(data){
                        if(data.hasOwnProperty('errors')) {
                            data.errors.forEach(function(val, idx, arr){
                                console.log(val);
                            });
                        }
                        else {
                            buckets.target_bucket.sources.push(buckets.target_source);
                        }
                    }
                });

                return true;
            }
            , 'configure_bucket_popup': function(){
                buckets.target_bucket = this;
                return true;
            }
            , 'configure_bucket': function(){
                $.ajax({
                    url: buckets_url + '/' + this.target_bucket.id
                    , type: 'POST'
                    , dataType: 'json'
                    , data: {
                        'description': this.target_bucket.description()
                        , 'schedule': this.target_bucket.schedule()
                    }
                    , success: function(data){
                        if(data.hasOwnProperty('errors')) {
                            data.errors.forEach(function(val, idx, arr){
                                console.log(val);
                            });
                        }
                        else {
                            $('#configure-bucket').popup('close');
                        }
                    }
                });

                return true;
            }
            , 'target_bucket': null
            , 'target_source': null
        }
        , tags = {
            'content': null
            , 'add_to_bucket_popup': function(source){
                buckets.target_source = source;
                return true;
            }
        }
        , scrollpos
    ;

    $('[data-role="panel"]')
        // when a panel is opened, remember the scroll position of the page
        .bind('panelopen', function(){
            scrollpos = $(window).scrollTop();
        })
        // when a panel is closed, restore the scroll position of the page
        .bind('panelclose', function(){
            $(window).scrollTop(scrollpos);
        })
    ;

    // when the 'content' panel is opened, focus on the search filter
    $('#content').bind('panelopen', function(){
        $('#content input[data-type="search"]').focus();
    });

    // pull tags and their sources
    $.get(tags_url, null, function(data){
        tags.content = ko.observableArray(data);
        ko.applyBindings(tags, $('#content')[0]);
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

        buckets.content = ko.observableArray(new_buckets);

        ['#add-to-bucket', '#buckets', '#remove-from-bucket', '#configure-bucket']
            .forEach(function(val, idx, arr){
                ko.applyBindings(buckets, $(val)[0]);
            })
        ;

        $('#buckets').trigger('create');
    }, 'json');
});
