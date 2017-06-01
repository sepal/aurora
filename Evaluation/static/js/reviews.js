$(function () {
    $(".review_answer").each(function () {
	    if (this.value == "") {this.style.height = '0px';} 
	    else {this.style.height = (this.scrollHeight-20)+'px';}
    });
});
