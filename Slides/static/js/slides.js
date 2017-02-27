$(function () {
	$('#slides-li').addClass('uRhere');
});

var myTimeout;

$(function() {
	$('.card-with-note').mouseover(function () {
			grayStuff(this.id);
			$(this).addClass('extraShadow');
	}).mouseleave(function () {
	    clearTimeout(myTimeout);
		$(this).removeClass('extraShadow');
		$('.lecturer_note').removeClass('grayout');	
	});
});

$(function() {
	$('.card-with').mouseover(function () {
			grayStuff(this.id);
			$(this).addClass('extraShadow');
	}).mouseleave(function () {
	    clearTimeout(myTimeout);
		$(this).removeClass('extraShadow');
		$('.lecturer_note').removeClass('grayout');	
	});
});


$(function() {
	$('.lecturer_note').mouseover(function () {
			grayText(this.id);
			$(this).addClass('extraShadowN');
	}).mouseleave(function () {
	    clearTimeout(myTimeout);
		$(this).removeClass('extraShadowN');
		$('.aCard').removeClass('grayout');	
	});
});

function grayStuff(x) {
	$('.lecturer_note').not('#LC_'+x.slice(3)).addClass('grayout');
}

function grayText(x) {
	$('.aCard').not('#SL_'+x.slice(3)).addClass('grayout')
}




$('#mylink').mouseenter(function() {
    myTimeout = setTimeout(function() {
    }, 500);
}).mouseleave(function() {
    clearTimeout(myTimeout);
});