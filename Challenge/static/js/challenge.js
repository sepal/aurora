$(function () {
    $('#challenges-li').addClass('uRhere');
    window.document.title = "Aurora: Challenges"
    $(".review_answer").each(function () {
        this.style.height = (this.scrollHeight+5)+'px';
    });
	$(".create_revision_link").click(function (){
		$('.create_revision').hide(300);
		$('.revision_section').show(300);

	})
});





$(challenge_loaded);

function challenge_loaded() {
    if ($('.elaboration_block').length) {
        init_tinymce();
        init_tinymce_read_only();
        init_tinymce_read_only_orig();
        $('.submit').click(submit_clicked);
		$('.save_back').click(go_back);
        $('.real_submit').click(real_submit_clicked);
        $('.real_submit_revised').click(real_submit_revised_clicked);
    } else {
        try {
            init_tinymce_read_only();
            init_tinymce_read_only_orig();
        } catch (err) {
            // TODO: improve!
        }
    }
}

function go_back() {
    var challenge = $('.challenge');
    var challenge_id = challenge.attr('id');
    elaboration_save(challenge_id);
	location.href = document.referrer;
}

function init_tinymce_read_only() {
    tinymce.init({
        // selector: "textarea#editor",
        mode: "exact",
        elements: "editor_challenge",
        menubar: false,
        statusbar: false,
        toolbar: false,
        height: 300,
//        plugins: "autoresize",
        autoresize_min_height: 300,
        autoresize_max_height: 800,
        readonly: 1,
        oninit: function () {
            var height = $('#editor_challenge_ifr').height() + 25;
            $('#editor_challenge_ifr').height(height);
        }
    });
}

function init_tinymce_read_only_orig() {
    tinymce.init({
        // selector: "textarea#editor",
        mode: "exact",
        elements: "editor_challenge_orig",
        menubar: false,
        statusbar: false,
        toolbar: false,
        height: 150,
//        plugins: "autoresize",
        autoresize_min_height: 150,
        autoresize_max_height: 800,
        readonly: 1

    });
}


var timeout;

function init_tinymce() {
    tinymce.init({
		paste_as_text:true,
        selector: "textarea#editor",
        paste_retain_style_properties: "font-size,bold,italic",
        paste_text_linebreaktype: "p",
        valid_elements: "p,strong,em,span[style],ul,ol,li,sub,br,sup,table,tbody,tr,td,div,hr",
        paste_preprocess: function (plugins, args) { // remove all links
            var content;
            try {
                content = $(args.content);
                if (content.selector === "") {
                    content.find('a').replaceWith(function () {
                        return $(this).text()
                    });
                    var fullHtml = "";
                    $(content).each(function () {
                        fullHtml += $(this).html();
                    });
                    args.content = fullHtml;
                }
            } catch (error) {
                // in case the content is not a valid markup
            }
        },
        menubar: false,
        theme: 'modern',
        statusbar: true,
        fontsize_formats: "0.8em 1em 1.2em 1.6em 2em",
        plugins: "autoresize paste wordcount",
        toolbar1: "undo redo | bold italic | fontsizeselect | bullist numlist indent outdent | hr",
        autoresize_min_height: 200,
        autoresize_max_height: 800,
		paste_data_images: false,
		setup: function(editor) {
			editor.on( 'keydown', function( args ) { if(timeout) {
			clearTimeout(timeout);
			timeout = null;
			}
			timeout = setTimeout(elaboration_save_intervalTimeOut, 1000) } );
		}
    });
}

function elaboration_save_intervalTimeOut() {
	var challenge = $('.challenge');
    var challenge_id = challenge.attr('id');
	clearTimeout(timeout);
	elaboration_autosave_notify(challenge_id);
	$('#saved_message').fadeIn(250).delay(3000).fadeOut(500);
}

function elaboration_autosave_notify(challenge_id) {
	revert_submit_clicked();
    elaboration_save(challenge_id);
}


function elaboration_autosave(e, challenge_id) {
    revert_submit_clicked();
    elaboration_save(challenge_id);
}

function elaboration_save(challenge_id, submit) {
    var elaboration_text = tinyMCE.activeEditor.getContent().toString();
    var data = {
        challenge_id: challenge_id,
        elaboration_text: elaboration_text,
        revised_elaboration_text: elaboration_text
    };
      console.log('Clicked real submit');
    var args = { type: "POST", url: SAVE_URL, data: data,
        success: function () {
            if (submit) {
                send_submit();
            }
        }
    };
    $.ajax(args);
}

function revised_elaboration_save(challenge_id, submit) {
    var elaboration_text = tinyMCE.activeEditor.getContent().toString();
    var changelog = $('#changelog').prop('value')
    var review_id = $("#most_helpful_other_user").val()
    var data = {
        challenge_id: challenge_id,
        revised_elaboration_text: elaboration_text,
        revised_elaboration_changelog: changelog,
        most_helpful_other_user: review_id
    };
    var args = { type: "POST", url: SAVE_URL, data: data,
        success: function () {
            if (submit) {
                send_revised_submit();
            }
        }
    };
    $.ajax(args);
}

function submit_clicked(event) {
    if (!$('#EWfE').hasClass('nope')) {
		clearTimeout(timeout);
		$('#saved_message').hide();
        $('.submit').hide().finish();
        $('.save_back').hide().finish();
        $('.submission_text').slideDown('fast',function(){window.scrollBy(0, 500);});
    }
}

function revert_submit_clicked() {
    $('.submit').show();
    $('.save_back').show();
    $('.submission_text').hide();
}

function real_submit_clicked(event) {
    var challenge = $('.challenge');
    var challenge_id = challenge.attr('id');
    elaboration_save(challenge_id, true);
}

function real_submit_revised_clicked(event) {
    var challenge = $('.challenge');
    var challenge_id = challenge.attr('id');
    revised_elaboration_save(challenge_id, true);
}

function send_submit() {
    var challenge = $('.challenge');
    var challenge_id = challenge.attr('id');
    var stack_id = challenge.attr('stack');
    ajax_setup();
    var data = {
        challenge_id: challenge_id,
        elaboration_text: tinyMCE.activeEditor.getContent().toString()
    };
    var args = { type: "POST", url: SUBMIT_URL, data: data,
        success: function () {
            window.location.href = STACK_URL + "?id=" + stack_id;
        },
        error: function () {
            alert("Error submitting elaboration!");
        }
    };
    $.ajax(args);
}

function send_revised_submit() {
    var challenge = $('.challenge');
    var challenge_id = challenge.attr('id');
    var stack_id = challenge.attr('stack');
    ajax_setup();
    var data = {
        challenge_id: challenge_id,
        revised_elaboration_text: tinyMCE.activeEditor.getContent().toString()
    };
    var args = { type: "POST", url: SUBMIT_URL, data: data,
        success: function () {
            window.location.href = STACK_URL + "?id=" + stack_id;
        },
        error: function () {
            alert("Error submitting elaboration!");
        }
    };
    $.ajax(args);
}
