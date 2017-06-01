$(function () {
    $(".review_answer").each(function () {
	    if (this.value == "") {this.style.height = '5px';} 
	    else {this.style.height = (this.scrollHeight+5)+'px';}
    });
});
