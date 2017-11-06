$(function() {
		$('#study_code').focus(function(){
			$('.correct_maker').removeClass('versteck',700);
		});
		$('.bmi').click(function(){
			$('#study_code').val('033532');
			$('#statement').focus();
			$('#study_code').change();
			$('.correct_maker').addClass('versteck',700);
		})
		$('.bmz').click(function(){
			$('#study_code').val('033533');
			$('#statement').focus();
      	  	$('#study_code').change();
			$('.correct_maker').addClass('versteck',700);
		})
		$('.bsi').click(function(){
			$('#study_code').val('033534');
			$('#statement').focus();
      	  	$('#study_code').change();
			$('.correct_maker').addClass('versteck',700);
		})
		$('.bti').click(function(){
			$('#study_code').val('033535');
			$('#statement').focus();
     	   	$('#study_code').change();
			$('.correct_maker').addClass('versteck',700);
		})
})


$(profile_loaded);

var file;

function profile_loaded() {
    $("input").change(input_change);
    $("#profile_avatar").click(file_upload_clicked);
    $("#file_upload_form").submit(submit_form);
    $("#error").hide();
}

function input_change(event) {
    ajax_setup()
    if (event.target.id === 'file_upload_input') {
        file = event.target.files[0];
        $("#file_upload_form").submit();
    } else {
        $.ajax({
            type: 'POST',
            url: PROFILE_SAVE_URL,
            data: {
                'nickname': $('#nickname').val(),
                'study_code': $('#study_code').val(),
                'statement': $('#statement').val(),
                'email': $('#email').val()
            },
            success: function (data) {
                var data = JSON.parse(data);
                if (data.error) {
                    $('#error').html(data.error);
                    $('#error').fadeIn(250).delay(5000).fadeOut(500);
                    $('#nickname').val(data.nickname);
                    $('#email').val(data.email);
                    $('#study_code').val(data.study_code);
                    $('#statement').val(data.statement);
                } else {
                    $('#error').html('');
                }
            }
        });
    }
}

function file_upload_clicked() {
    $('#file_upload_input').trigger('click');
}

function submit_form(event) {
    event.stopPropagation();
    event.preventDefault();
    var data = new FormData();
    data.append('file', file);

    data.append('user_id', $('#user_id').val());
    $.ajax({
        url: '/fileupload',
        type: 'POST',
        data: data,
        cache: false,
        dataType: 'json',
        processData: false,
        contentType: false,
        complete: function (data) {
            location.reload();
        }
    });
}

function create_new_feed_token(url) {
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
    }).done(function(data) {
        $('#feed_token').val(data.token);
    })
}

