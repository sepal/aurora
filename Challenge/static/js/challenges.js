$(function() {
	$('.filterbar').each(function () {
        $(this).css('background-position-x', (Math.floor(Math.random()*50)+50)+'%');
        $(this).css('background-position-y', (Math.floor(Math.random()*100))+'%');
	})
})

$(function() {
	$('#challenges-li').addClass('uRhere');
	window.document.title="Aurora: Challenges";

	// $("#titleSort").on("click", function () {
	//
	//     var wrapper = $('#detail_area'),
	//         art = wrapper.children('.stack');
	//
	//     art.sort(function(a, b) {
	//         return $(a).data('title').localeCompare($(b).data('title'));
	//     })
	//     .each(function() {
	//         wrapper.append(this);
	//     });
	// });
	//
	// $("#statusSort").on("click", function () {
	//     var $wrapper = $('#detail_area'),
	//         $art = $wrapper.children('.stack');
	//
	//     $art.sort(function(a, b) {
	//         return +$(a).data('status') > +$(b).data('status') ? 1 : -1;
	//     })
	//     .each(function() {
	//         $wrapper.append(this);
	//     });
	// });
	//
	//
	// $("#chapterSort").on("click", function () {
	//
	//     var $wrapper = $('#detail_area'),
	//         $art = $wrapper.children('.stack');
	//
	//     $art.sort(function(a, b) {
	//         return $(a).data('chapter').localeCompare($(b).data('chapter'));
	//     })
	//     .each(function() {
	//         $wrapper.append(this);
	// 	});
	// });
	//
	//
	// $("#dateSort").on("click", function () {
	// 	location.reload();
	// 	/*
	//     var $wrapper = $('#detail_area'),
	//         $art = $wrapper.children('.stack');
	//
	//     $art.sort(function(a, b) {
	//         return +$(a).attr('ID') < +$(b).attr('ID') ? 1 : -1;
	//     })
	//     .each(function() {
	//         $wrapper.append(this);
	// 	});
	// 	*/
	// });


	$('.filterbar').click(function (){
		$('.filter_'+$(this).data('filter')).toggleClass('shrinked',300);
	})
	

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

