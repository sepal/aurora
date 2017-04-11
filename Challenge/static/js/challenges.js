$(function() {
	$('.filterbar').each(function () {
        $(this).css('background-position-x', (Math.floor(Math.random()*50)+50)+'%');
        $(this).css('background-position-y', (Math.floor(Math.random()*100))+'%');
	})
	$('#challenges-li').addClass('uRhere');
	window.document.title="Aurora: Challenges " + course_short_title;

	$('.filterbar').click(function (){
		$('.filter_'+$(this).data('filter')).toggleClass('shrinked',300);
		setTimeout(chapterCookieUpdate,350);
	})
	chapterCookieLoad();
});


$(challenges_loaded);

function challenges_loaded() {
    $(".stack:not(.forbiddenfruit)").click(stack_clicked);
    $(".stack.allowedfruit").click(stack_clicked);
}

function stack_clicked(event) {
    var stack = $(event.target).closest(".stack");
    var stack_id = stack.attr('id');
    window.location.href = './stack?id=' + stack_id;
}

function sortC(a,b) {
	return a.getElemetsByClassName('description')[0] > b.getElementsByClassName('description')[0] ? 1 : -1;
}

function doSort(sType) {
	$('.detail_area .stack').sort(sortC).appendTo('detail_area');
}



function chapterCookieUpdate() {
    "use strict";
	var newChapterC = ""
	$('.filterbar').each(function() {
		var aChapterID = '.filter_' + $(this).data('filter');
		if ($(aChapterID).hasClass('shrinked')) {
			newChapterC = newChapterC + "," + $(this).data('filter');
		}
	});
	newChapterC = newChapterC.substr(1);
    document.cookie = "chapterCookie." + $('#the_username').data('username') + "= " + newChapterC + "; expires=Tue, 18 Jan 2038 03:14:06 GMT";
}

function chapterCookieLoad() {
	fCookie = getCookie('chapterCookie.' + $('#the_username').data('username'));
	if (fCookie != null) {
		var clickedChapters = fCookie.split(',');
		for (var i = 0; i < clickedChapters.length; i++) {
			$('.filter_'+clickedChapters[i]).toggleClass('shrinked',0);
		}
    }
}
