// #####################
//  Setup
// #####################
var trixDings;

$(document).ready(function() {
    $('#challenges-li').addClass('uRhere');
    $(".review_answer").each(function() {
        this.style.height = (this.scrollHeight + 5) + 'px';
    });

    $(".create_revision_link").click(function() {
        $('.create_revision').hide(300);
        $('.revision_section').show(300);
    });
	$(".zustimmung").click(function(){
		if ($('#zustimmungs_box').prop('checked')) {$('.real_submit').removeClass('cannot_submit')} else {$('.real_submit').addClass('cannot_submit')}
	});
	$('.see_through').focus(function () {
		$('.input_position').removeClass('see_through');
	});
	$('.zustimmungstext').click(function() {
		$('#zustimmungs_box').prop( "checked", true );
		$('.real_submit').removeClass('cannot_submit');
	});
	trixDings = document.querySelector("trix-editor");
	document.addEventListener('trix-change',countChars);
	document.addEventListener('trix-initialize',countChars);
});

$(challenge_loaded);

function countChars() {
	var x = trixDings.editor.getDocument().toString();
	$('.new_word_count').text(x.replace(/^[\s,.;]+/, "").replace(/[\s,.;]+$/, "").split(/[\s,.;]+/).length);
}

function challenge_loaded() {
    // Register event handlers
    if ($('.elaboration_block').length) {
        $('.submit').click(submit_clicked);
        $('.save_back').click(go_back);
        $('.real_submit').click(real_submit_clicked);
        $('.real_submit_revised').click(real_submit_revised_clicked);
    }

    // Dont allow inline files
    document.addEventListener("trix-file-accept", function(event) {
        event.preventDefault();
        return
    });

    $(".submitted-content > trix-editor").attr('contenteditable', 'false');

    // Autosafe elaboration every x milliseconds
    var autosave_interval = 10000
    window.setInterval(function() {
        var challenge_id = $('.challenge').attr('id');
        save_elaboration(challenge_id);
    }, autosave_interval);
}

// #####################
//  Elaboration
// #####################

function submit_clicked() {
    var challenge_id = $('.challenge').attr('id');
    save_elaboration(challenge_id);
    $('#saved_message').hide();
    $('.submit').hide().finish();
    $('.save_back').hide().finish();
    $('.hidden_extra_question').slideDown('fast');
    $('.submission_text').slideDown('fast', function() {
        window.scrollBy(0, 500);
    });
}

function real_submit_clicked() {
    var challenge_id = $('.challenge').attr('id');
    save_elaboration(challenge_id);
    submit_elaboration(challenge_id);
}

function go_back() {
    var challenge_id = $('.challenge').attr('id');
    save_elaboration(challenge_id);
    location.href = document.referrer;
}

function revert_submit_clicked() {
    $('.submit').show();
    $('.save_back').show();
    $('.submission_text').hide();
}

function save_elaboration(challenge_id) {
    // Don't save the elaboration if a revision is possible
    if ($("#revised-editor").length) {
        return;
    }

    // Dont do anything if the editor is not present
    if($("#original-editor").length == 0) {
      return;
    }


    var elaboration_text = $("#original-editor").val();
    var extra_review_question = $("#extra-review-question").val();
    var data = {
        challenge_id: challenge_id,
        elaboration_text: elaboration_text,
        revised_elaboration_text: elaboration_text,
        extra_review_question: extra_review_question
    };

    var args = {
        type: "POST",
        url: SAVE_URL,
        async: false,
        data: data
    };

    $.ajax(args);
}

function submit_elaboration(challenge_id) {
    ajax_setup();
    var data = {
        challenge_id: challenge_id
    }

    var args = {
        type: "POST",
        url: SUBMIT_URL,
        async: false,
        data: data,
        success: function() {
            window.location.href = STACK_URL + "?id=" + $('.challenge').attr('stack');
        },
        error: function() {
            alert("Error submitting elaboration!");
        }
    };
    $.ajax(args);
}


// #####################
//  Revised Elaboration
// #####################

function save_revised_elaboration(challenge_id) {
    // Exit early if ther is no revised editor present
    if (!$("#revised-editor").length) {
        return;
    }

    var revised_elaboration_text = $("#revised-editor").val();
    var changelog = $('#changelog').prop('value');
    var review_id = $("#most_helpful_other_user").val();

    var data = {
        challenge_id: challenge_id,
        revised_elaboration_text: revised_elaboration_text,
        revised_elaboration_changelog: changelog,
        most_helpful_other_user: review_id
    };

    var args = {
        type: "POST",
        url: SAVE_REVISION_URL,
        async: false,
        data: data,
    };

    $.ajax(args);
}

function submit_revised_elaboration(challenge_id) {
    var changelog = $('#changelog').prop('value');
    var review_id = $("#most_helpful_other_user").val();

    if (isNaN(review_id)) {
        alert("Please select something from the »most helpful« menu, thank you!");
        return false
    }
    if (changelog.length < 15) {
        alert("Please write a meaningful changelog, thank you!");
        return false
    }

    save_revised_elaboration(challenge_id)
}

function real_submit_revised_clicked() {
    var challenge_id = $('.challenge').attr('id');
    var saved = submit_revised_elaboration(challenge_id)
      location.href = document.referrer;
}
