
$(function(){
	$('.card_text').ellipsis({
	    row: 9,
		char: '… (click for full text)',
	    onlyFullWords: true
	});
	$('#challenges-li').addClass('uRhere');
});




$(stack_loaded);



function status_text(status_ID) {
	if (status_ID == -1) 
		{return "Can not be submitted yet."}
	else 
		{
			msgs = [
				"Not started (Click card to proceed).",
				"Not submitted.",
				"Waiting for you to write a review",
				"Bad review. We need to look at this. Please be patient.",
				"Done, waiting for reviews by others.",
				"Done, peer reviewed.",
				"Waiting for evaluation.",
				"Evaluated."];
				return msgs[status_ID];
		}
}



function stack_loaded() {
	$(".card").click(challenge_clicked);
    $(".review_box.active").click(review_box_clicked);
    $(".review_box.in_progress").click(review_box_clicked);
    $(".review_box.done").click(done_review_box_clicked);
    $(".received_review").click(received_review_clicked);
	$(".s3").click(show_reviews)
	$(".card_reviews").click(close_reviews)
}

function close_reviews(event) {
	$('#'+this.id).fadeToggle(400);
	event.stopPropagation();
}

function show_reviews(event) {
	$("#R"+this.id).fadeToggle(400);
	event.stopPropagation();
}

function challenge_clicked(event) {
    event.stopPropagation();
    var challenge = $(event.target).closest(".card");
    var challenge_id = challenge.attr('challenge_id');
    window.location.href = './challenge?id=' + challenge_id
}

function review_box_clicked(event) {
    event.stopPropagation();
    var challenge_id = $(event.target).parent().attr('challenge_id');
    window.location.href = REVIEW_URL + '?id=' + challenge_id;
}

//add done_review_box_clicked function here
function done_review_box_clicked(event) {
    event.stopPropagation();
    var challenge_id = $(event.target).parent().attr('challenge_id');;
    window.location.href = 'myreviews?id=' + challenge_id;
}

function received_review_clicked(event) {
    event.stopPropagation();
    var challenge = $(event.target).parent().parent();
    var challenge_id = challenge.attr('challenge_id');
    window.location.href = './challenge?id=' + challenge_id
}
