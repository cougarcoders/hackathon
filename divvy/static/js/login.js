/* login for divvy */
define(['global', 'jquery', 'jquery-mobile'], function(global, $, $m){
    // focus on the username field when we load the page
    $(document).bind('pageshow', '#login-page', function(e) {
        $('#username').focus();
    });
});
