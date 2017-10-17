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

function toggle_notification_field(elmt) {
    var field = $(elmt).parent().children('#notification_field')
    if (field.css('display') === 'block') {
        field.css('display', 'none');
    } else {
        field.css('display', 'block');
    }
    //$(elmt).closest('#notification_field').css('display', 'block');
}

function close_notification_field(elmt) {
    $(elmt).parent().parent().css('display', 'none');
}

function send_notification(elmt, course_short_title) {
    var form = $(elmt).parent('form');
    var url = '/course/' + course_short_title + '/notifications/send'

    $.ajax({
        type: 'POST',
        url: url,
        data: form.serializeArray()
    }).done(function() {
        form.parent().css('display', 'none');
    }).fail(function() {
        console.log('error');
    });
}