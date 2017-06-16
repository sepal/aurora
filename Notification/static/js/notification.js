function notifications_loaded() {
    $('#read_all_button').click(read_all_button_clicked);
	$('#notifications-li').addClass('uRhere');
	window.document.title="Aurora: Notifications"
}

$(notifications_loaded);

function read_all_button_clicked(event) {
    $.get(READ_URL, function (data) {
        location.reload();
    });
}

function open_notification_field(elmt) {
    $(elmt).parent().children('#notification_field').css('display', 'block');
}

function send_notification(elmt, course_short_title) {
    form = $(elmt).parent('form');
    url = '/' + course_short_title + '/notifications/send'

    $.ajax({
        type: 'POST',
        url: url,
        data: form.serializeArray()
    }).done(function() {
        form.parent().css('display', 'none');
    }).error(function() {
        console.log('error');
    });
}