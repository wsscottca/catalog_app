(function($) {
    var $window = $(window)
    // On window resize change classes between mobile and desktop views
    function resize(){
        if ($window.width() > 905) {
        	$(".dropdown").addClass("hidden");
        	$(".cat-nav").removeClass("hidden");
        	$(".index-main").addClass("well");
        	$(".catalog").addClass("col-sm-5");
        	$(".catalog").removeClass("col-xs-12");
        	$(".index").addClass("col-sm-5");
        	$(".index").removeClass("col-xs-12");
        	return true;
        } else if ($window.width() < 905){
        	$(".dropdown").removeClass("hidden");
        	$(".cat-nav").addClass("hidden");
        	$(".index-main").removeClass("well");
        	$(".catalog").addClass("col-xs-12");
        	$(".catalog").removeClass("col-sm-5");
        	$(".index").addClass("col-sm-5");
        	$(".index").removeClass("col-xs-12");
        	return true;
        }
    }

    $window.resize(function(){resize()}).trigger('resize');
})(jQuery);