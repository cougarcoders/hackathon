/* global functionality for divvy */
define(['jquery', 'jquery-mobile'], function($, $m){
    // used for window resize stagger
    var t;

    // stagger window resize event to avoid unnecessary cycles
    $(window).bind('resize', function(){
        clearTimeout(t);
        t = setTimeout(function(){
            // fit the panels to the page height
            $('.ui-panel').height($('.ui-page').height());
        }, 10);
    });

    // reflow content when the page is shown
    $(document).bind('pageshow', function(){
        $(window).trigger('resize');
    });
});
