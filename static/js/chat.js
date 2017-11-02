var chatupdate_timer_ID;
var chat_msgs = 0;

$(function(){
	setTimeout(function() {chat_msgs = $('.MessageList').children().length; chatupdate();},1000);
})

function chatupdate()
{
	if($('#small_talk').css('display')=='block') {
		$('#small_talk').scrollTop($('#small_talk')[0].scrollHeight);
		$('#chat_activity').text('');	
		chat_msgs = $('.MessageList').children().length;
	} else {
		newL = $('.MessageList').children().length;
		if (newL > chat_msgs) {
			$('#chat_activity').text('💬 '.repeat(Math.round(Math.log((newL - chat_msgs)*2))));			
		} 
	}
	chatupdate_timer_ID = setTimeout(chatupdate,1000);
}

