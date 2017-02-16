$(function () {
	$('#slides-li').addClass('uRhere');
});

$(function() {
	$('.aCard').hover(
		function () {
			$('#LC_'+this.id.slice(3)).toggleClass('extraShadow');
	});
});


$(function() {
	$('.lecturer_note').hover(
		function () {
			$('#SL_'+this.id.slice(3)+' img').toggleClass('extraShadowXL');
	});
});

