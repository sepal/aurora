// #####################
//  Setup
// #####################

$(document).ready(function() {
    $('#challenges-li').addClass('uRhere');
    $(".review_answer").each(function() {
        this.style.height = (this.scrollHeight + 5) + 'px';
    });

    $(".create_revision_link").click(function() {
        $('.create_revision').hide(300);
        $('.revision_section').show(300);
    })

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

    // Autosafe elaboration every x milliseconds
    var autosave_interval = 20000
    window.setInterval(function() {
        console.log("Interval save");
        var challenge_id = $('.challenge').attr('id');
        save_elaboration(challenge_id);
    }, autosave_interval);
});

// #####################
//  Elaboration
// #####################

function submit_clicked() {
    $('#saved_message').hide();
    $('.submit').hide().finish();
    $('.save_back').hide().finish();
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

    // Wait one second before actually redirecting to ensure
    // the ajax request to save the elaboration gets sent
    window.setInterval(function() {
        location.href = document.referrer;
    }, 1000);
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

    var elaboration_text = $("#original-editor").val();
    var data = {
        challenge_id: challenge_id,
        elaboration_text: elaboration_text,
        revised_elaboration_text: elaboration_text
    };

    var args = {
        type: "POST",
        url: SAVE_URL,
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
    var changelog = $('#changelog').prop('value')
    var review_id = $("#most_helpful_other_user").val()

    var data = {
        challenge_id: challenge_id,
        revised_elaboration_text: revised_elaboration_text,
        revised_elaboration_changelog: changelog,
        most_helpful_other_user: review_id
    };

    var args = {
        type: "POST",
        url: SAVE_URL,
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

    if (saved != false) {
        // Wait one second before actually redirecting to ensure
        // the ajax request to save the elaboration gets sent
        window.setInterval(function() {
            location.href = document.referrer;
        }, 1000);
    };
}
