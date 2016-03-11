var quotePost = "";
var quotePostMarkdown = "";

function diskursReply() {
    var parent = $(this).parent().parent().parent();
    parent.siblings().each(function () {
        if (!$(this).is(parent)) {
            $(this).removeClass('show_child');
        };
    });
    $('.show_reply').removeClass('show_reply');
    parent.addClass('show_child show_reply');
    parent.parent().addClass('show_child');
    parent.find('textarea').focus();
}

function diskursNewPost(e) {
    var form = $(this);
    var postData = form.serializeArray();
    var formURL = form.attr('action');
    $.ajax({
        url : formURL,
        type: "POST",
        data : postData,
        success:function(data, textStatus, jqXHR)
        {
            if (data.success) {
                form.parent().before(data.post);
                form.parent().parent().parent().addClass('has_children');
                var count = parseInt(form.parent().parent().parent().children('.container').children('.post_header').children('.count').html()) + 1;
                form.parent().parent().parent().children('.container').children('.post_header').children('.count').html(count);
                form.parent().prev().children('.container').children('.post_content').readmore({
                    speed: 75,
                    lessLink: '<a class="read_less" href="#">Read less</a>',
                    moreLink: '<a class="read_more" href="#">Read more</a>'
                });
                form.find('textarea').val('');
                form.parent().parent().parent().removeClass('show_reply');
            } else {
                alert(data.message);
            }
        },
    });
    e.preventDefault();
}

function diskursShowPost(element) {
    var parent = element.parent();
    parent.addClass('show_child');
    parent.siblings().each(function () {
        if (!$(this).is(parent)) {
            $(this).removeClass('show_child');
        };
    });
    parent.parent().addClass('show_child');
    parent.find('.show_child').removeClass('show_child');
}

function diskursHidePost(element) {
    element.parent().removeClass('show_child');
    element.parent().parent().removeClass('show_child');
}

function diskursShowPostClick() {
    if ($(this).parent().hasClass('show_child')) {
        diskursHidePost($(this));
        var prev = $(this).parent().parent().prev('.arrow_wrapper')
        history.pushState({post: '#'+prev.attr('id')}, '', prev.attr('href'));
    } else {
        diskursShowPost($(this));
        history.pushState({post: '#'+$(this).attr('id')}, '', $(this).attr('href'));
    }
    return false;
}

function isPicURL(url) {
    return(url.match(/^http.+\.(jpeg|jpg|gif|png|tiff|bmp)$/) != null);
}

function isURL(url) {
    return(url.match(/^http/) != null);
}

$(document).ready(function() {
    $('.level1').on('click', 'a.arrow_wrapper', diskursShowPostClick);
    $('.level0 > a.arrow_wrapper').click(function() { return false; });
    $('#diskurs').on('click', '.reply', diskursReply);
    $('#diskurs').on('submit', 'form', diskursNewPost);
    $('.post_content').readmore({
        speed: 75,
        lessLink: '<a class="read_less" href="#">Read less</a>',
        moreLink: '<a class="read_more" href="#">Read more</a>'
    });

    $('#diskurs').on('click', '.toggle_emojipicker', function() {

        $(this).prev().prev().prev().emojiPicker({
            width: '300px',
            height: '200px',
            button: false
        });

        $(this).prev().prev().prev().emojiPicker('toggle');
    });

    $('#diskurs').on('click', 'a.upvote', function(e) {
        e.preventDefault();

        var votes = $(this).parent().parent().find('.votes');
        url = $(this).attr('href');
        upvote = $(this).parent().find('.upvote');
        downvote = $(this).parent().find('.downvote');

        $.ajax({
            url: url,
            success:function(data, textStatus, jqXHR)
                {
                    if (data.success) {
                        votes.text(data.sum);
                        upvote.addClass('marked');
                        downvote.removeClass('marked');
                    } else if (data.removed) {
                        votes.text(data.sum);
                        upvote.removeClass('marked');
                        downvote.removeClass('marked');
                    } else {
                        alert(data.message);
                    }
                },
        });
    });

    $('#diskurs').on('click', 'a.downvote', function(e) {
        e.preventDefault();

        votes = $(this).parent().parent().find('.votes');
        url = $(this).attr('href');
        upvote = $(this).parent().find('.upvote');
        downvote = $(this).parent().find('.downvote');

        $.ajax({
            url: url,
            success:function(data, textStatus, jqXHR)
                {
                    if (data.success) {
                        votes.text(data.sum);
                        upvote.removeClass('marked');
                        downvote.addClass('marked');
                    } else if (data.removed) {
                        votes.text(data.sum);
                        upvote.removeClass('marked');
                        downvote.removeClass('marked');
                    } else {
                        alert(data.message);
                    }
                },
        });
    });

    $('#diskurs').on('click', 'a.delete', function(e) {
        e.preventDefault();

        content = $(this).parent().parent().parent();
        url = $(this).attr('href');

        $.ajax({
            url: url,
            success:function(data, textStatus, jqXHR)
                {
                    if (data.success) {
                        content.replaceWith(data.content);
                    } else {
                        alert(data.message);
                    }
                },
        });
    });

    $('#diskurs').on('copy', '.post_content', function(e) {
        quotePost = String(window.getSelection()).trim();
        quotePostMarkdown = $(this).prev().find('.user').text() + ' wrote:\n' + '> ' + quotePost.replace('\n', '\n> ') + '\n\n';
    })

    $('#diskurs').on('paste', 'textarea.reply_area', function(e) {
        var clipboardData = e.originalEvent.clipboardData.getData('text/plain').trim();
        var insertText = false;

        if (isPicURL(clipboardData)) {
            insertText = '![](' + clipboardData + ' "")\n';
        } else if (isURL(clipboardData)) {
            insertText = '[link](' + clipboardData + ') ';
        } else if (clipboardData == quotePost) {
            insertText = quotePostMarkdown;
        }

        if (insertText) {
            $(this).insertAtCaret(insertText);
            e.preventDefault();
        }
    })
});

window.onpopstate = function(event) {
    if (event.state != null) {
        diskursShowPost($(event.state.post));
    } else {
        $('#diskurs').find('.show_child').removeClass('show_child');
    }
};