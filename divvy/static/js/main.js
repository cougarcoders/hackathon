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
        errors = ko.observableArray()
        , buckets = {
            'content': null
            , 'remove_from_bucket_popup': function(source, bucket){
                buckets.target_bucket(bucket);
                buckets.target_source(source);
                return true;
            }
            , 'remove_from_bucket': function(){
                var
                    bucket = buckets.target_bucket()
                    , source = buckets.target_source()
                ;

                $.ajax({
                    url: buckets_url + '/' + bucket.id + '/' + source.id
                    , type: 'DELETE'
                    , dataType: 'json'
                    , success: function(data){
                        if(data.hasOwnProperty('errors')) {
                            errors(data.errors);
                            $('#errors').popup('open');
                        }
                        else {
                            bucket.sources.splice(bucket.sources.indexOf(source), 1);
                        }
                    }
                });

                return true;
            }
            , 'add_to_bucket': function(){
                var
                    bucket = buckets.target_bucket()
                    , source = buckets.target_source()
                ;

                $.ajax({
                    url: buckets_url + '/' + bucket.id + '/' + source.id
                    , type: 'PUT'
                    , dataType: 'json'
                    , success: function(data){
                        if(data.hasOwnProperty('errors')) {
                            errors(data.errors);
                            $('#errors').popup('open');
                        }
                        else {
                            bucket.sources.push(source);
                        }
                    }
                });

                return true;
            }
            , 'configure_bucket_popup': function(){
                var $sched = $('#bucket-schedule');
                buckets.target_bucket(this);
                $sched.prev('span').text($sched.find('option:selected').text());
                return true;
            }
            , 'configure_bucket': function(){
                var
                    bucket = this.target_bucket()
                    , sched = $('#bucket-schedule').val()
                ;

                $.ajax({
                    url: buckets_url + '/' + bucket.id
                    , type: 'POST'
                    , dataType: 'json'
                    , data: {
                        'description': bucket.description()
                        , 'schedule': sched
                    }
                    , success: function(data){
                        if(data.hasOwnProperty('errors')) {
                            errors(data.errors);
                            $('#errors').popup('open');
                        }
                        else {
                            bucket.schedule(sched);
                            $('#configure-bucket').popup('close');
                        }
                    }
                });

                return true;
            }
            , 'target_bucket': ko.observable()
            , 'target_source': ko.observable()
        }
        , tags = {
            'content': null
            , 'add_to_bucket_popup': function(source){
                buckets.target_source(source);
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

        ko.applyBindings(errors, $('#errors')[0]);
        $('#buckets').trigger('create');
    }, 'json');
});
