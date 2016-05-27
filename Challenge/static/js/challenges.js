$(function() {
	$('#challenges-li').addClass('uRhere');
	window.document.title="Aurora: Challenges";

	$("#titleSort").on("click", function () {
    
	    var wrapper = $('#detail_area'),
	        art = wrapper.children('.stack');
			
	    art.sort(function(a, b) {
	        return $(a).data('title').localeCompare($(b).data('title'));
	    })
	    .each(function() {
	        wrapper.append(this);
	    });
		$('#detail_area').masonry('reloadItems');
		$('#detail_area').masonry('layout');
	});

	$("#statusSort").on("click", function () {
	    var $wrapper = $('#detail_area'),
	        $art = $wrapper.children('.stack');
		
	    $art.sort(function(a, b) {
	        return +$(a).data('status') > +$(b).data('status') ? 1 : -1;
	    })
	    .each(function() {
	        $wrapper.append(this);
	    });
		$('#detail_area').masonry('reloadItems');
		$('#detail_area').masonry('layout');
	});


	$("#chapterSort").on("click", function () {
    
	    var $wrapper = $('#detail_area'),
	        $art = $wrapper.children('.stack');

	    $art.sort(function(a, b) {
	        return $(a).data('chapter').localeCompare($(b).data('chapter'));
	    })
	    .each(function() {
	        $wrapper.append(this);
		});
		$('#detail_area').masonry('reloadItems');
		$('#detail_area').masonry('layout');
	});


	$("#dateSort").on("click", function () {
		location.reload();
		/*
	    var $wrapper = $('#detail_area'),
	        $art = $wrapper.children('.stack');

	    $art.sort(function(a, b) {
	        return +$(a).attr('ID') < +$(b).attr('ID') ? 1 : -1;
	    })
	    .each(function() {
	        $wrapper.append(this);
		});
		$('#detail_area').masonry('reloadItems');
		$('#detail_area').masonry('layout');
		*/
	});
	$('#detail_area').masonry({itemSelector:'.stack',columWidth:0})

});


$(challenges_loaded);

function challenges_loaded() {
    $(".stack:not(.forbiddenfruit)").click(stack_clicked);
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

