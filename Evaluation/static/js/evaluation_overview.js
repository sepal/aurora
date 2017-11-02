$.fn.redraw = function(){
  $(this).each(function(){
    var redraw = this.offsetHeight;
  });
};

$(document).ready(function() {
    $(".tab-content").first().css("display", "block");

    $(".tabs-menu a").click(function(event) {
        event.preventDefault();
        $(this).parent().addClass("current");
        $(this).parent().siblings().removeClass("current");
        var tab = $(this).attr("href");
        $(".tab-content").not(tab).css("display", "none");
        $(tab).fadeIn();

        $(".review_answer").each(function () {
    	    if (this.value == "") {this.style.height = '0px';} 
    	    else {this.style.height = (this.scrollHeight)+'px';}
        });
        $('.review_answer').redraw();
		EcountChars();
    });
	$("trix-editor").attr('contenteditable', 'false');
	updateWordCount();
});

function updateWordCount() {
	var trixies = document.querySelectorAll('trix-editor');

	[].forEach.call(trixies, function(trixie) {
		theTrix = $(trixie).attr('data-ID');
		try { 
			var x = trixie.editor.getDocument().toString();
			$('#'+theTrix).text(x.replace(/^[\s,.;]+/, "").replace(/[\s,.;]+$/, "").split(/[\s,.;]+/).length);
		}
		catch(m) {
			alert(m);
		}
	});
}

function EcountChars() {
/*	
	var trixDings = document.querySelector("trix-editor");
	var x = trixDings.editor.getDocument().toString();
	$('.new_word_count').text(x.replace(/^[\s,.;]+/, "").replace(/[\s,.;]+$/, "").split(/[\s,.;]+/).length);
	trixDings = document.querySelector("#trix2");
	x = trixDings.editor.getDocument().toString();
	$('.new_word_count_2').text(x.replace(/^[\s,.;]+/, "").replace(/[\s,.;]+$/, "").split(/[\s,.;]+/).length);
*/
}

$(function() {
    $(".submit_evaluation").click(function(event) {
        event.preventDefault();

        var points = Math.abs(parseInt($(".points").text()) || 0);
        if ($.trim($(".evaluation").text()).length == 0) {
            $(".error").html("you forgot feedback!");
            return;
        }
        var data = {
            elaboration_id: $(event.target).attr('id'),
            evaluation_text: $(".evaluation").html(),
            evaluation_points: points
        };
        var args = {
            type: "POST",
            url: "./submit_evaluation/",
            data: data,
            async: false,
            error: function() {
                alert('error submitting evaluation');
            },
            success: function() {
              var next = $(event.target).data('next-id');
              if(next) {
                window.location.href = "./overview?elaboration_id=" + next;
              } else {
                  window.location.reload();
              }

            }
        };
        $.ajax(args);
    });
});

$(function() {
    $(".reopen_evaluation").click(function(event) {
        event.preventDefault();
        var data = {
            elaboration_id: $(event.target).attr('id')
        };
        var args = {
            type: "POST",
            url: "./reopen_evaluation/",
            data: data,
            success: function() {
                // var url = './detail?elaboration_id=' + $(event.target).attr('id');
                // $.get(url, function (data) {
                //     $('body').html(data);
                // });
                window.location.reload();
            }
        };
        $.ajax(args);
    });
});


var timer = 0;

function StartEvaluation(elaboration_id) {
    var url = './start_evaluation?elaboration_id=' + elaboration_id;
    $.get(url, function(state) {
        if (state == 'init') {
            $('.evaluation').html("");
            $('.points').attr('contentEditable', true);
        }
        if (state == 'open') {
            $('.evaluation').attr('contentEditable', true);
            $('.points').attr('contentEditable', true);
        }
        if (state.indexOf('locked') > -1) {
            $('.evaluation').html("<div class='evaluation_lock'>" + state + "</div>")
            $('.evaluation').attr('contentEditable', false);
            $('.points').attr('contentEditable', false);
        }
    });
}

function DelayedAutoSave(elaboration_id) {
    if (timer)
        window.clearTimeout(timer);
    timer = window.setTimeout(function() {
        AutoSave(elaboration_id);
    }, 500);
}

function AutoSave(elaboration_id) {
    var points = Math.abs(parseInt($(".points").text()) || 0);
    var data = {
        elaboration_id: elaboration_id,
        evaluation_text: $(".evaluation").html(),
        evaluation_points: points
    };
    var args = {
        type: "POST",
        url: "./save_evaluation/",
        data: data,
        error: function() {
            alert('error saving evaluation');
        }
    };
    $.ajax(args);
}
