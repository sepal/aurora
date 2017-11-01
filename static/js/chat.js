var chatupdate_timer_ID;

function chatupdate()
{
	$('#small_talk').scrollTop($('#small_talk')[0].scrollHeight);
	chatupdate_timer_ID = setTimeout(chatupdate,1000);
}

function stop_chatupdate() {
	clearTimeout(chatupdate_timer_ID);
}