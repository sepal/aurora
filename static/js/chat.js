var chatupdate_timer_ID;
var chat_msgs = 0;
var chat_scroll = 'Y';

$(function(){
	setTimeout(function() {chat_msgs = $('.MessageList').children().length; chatupdate();},1000);
	chat_scroll = 'Y';
/*	$("#small_talk").scroll(function() {
		if (chat_scroll == 'A') {
			chat_scroll = 'Y';
		} else if (chat_scroll == 'M') {
			if ($('#small_talk').scrollTop() == $('#small_talk')[0].scrollHeight) {chat_scroll = 'Y'}
			
		} else {
			chat_scroll = 'M';
		}
	}); */
})

function chatupdate()
{
  if (chat_scroll == 'Y') {
		if($('#small_talk').css('display')=='block') {
			$('#chat_activity').text('');
			chat_msgs = $('.MessageList').children().length;
		} else {
			newL = $('.MessageList').children().length;
			if (newL > chat_msgs) {
				$('#chat_activity').text('💬 '.repeat(Math.round(Math.log((newL - chat_msgs)*2))));			
			} 
		}
	}
	chatupdate_timer_ID = setTimeout(chatupdate,2000);
}

