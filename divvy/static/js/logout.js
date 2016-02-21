/* logout for divvy */
define(['global', 'jquery', 'jquery-mobile'], function(global, $, $m){
    // redirect to the homepage after a delay
    setTimeout(function(){ $.mobile.navigate('/'); }, 7000);
});
