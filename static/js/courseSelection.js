//get last page from history, add ur to link.
	var comeFrom = document.referrer.split('/');
	var appendix = "";
	if (comeFrom.indexOf("challenge") != -1) {appendix = 'challenge/'}
	else if (comeFrom.indexOf("slides") != -1) {appendix = 'slides/'}
	else if (comeFrom.indexOf("evaluation") != -1) {appendix = 'evaluation/'}

$(function() {$('.xURL').each(function(){
	$(this).attr('href',$(this).attr("href") + appendix);
})})
