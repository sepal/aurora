$(function() {
    $(".paginator_others").click(function(event) {
        var url = './others?page=' + $(event.target).attr('id');
        $.get(url, function (data) {
            $('#info_area').html(data);
        });
    });
});

$(function () {
    $(".review_answer").each(function () {
        this.style.height = (this.scrollHeight+5)+'px';
    });
});

$(document).ready(function() {
  $("trix-editor").attr('contenteditable', 'false');
});
