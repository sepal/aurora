var quotePost = "";
var quotePostMarkdown = "";

function diskursReply() {
    var parent = $(this).parent().parent().parent();
    var arrow = parent.children('.arrow_wrapper').first();

    if (parent.hasClass('show_child')) {
        history.pushState({post: '#'+$(arrow).attr('id')}, '', $(arrow).attr('href'));
    } else {
        diskursShowPost(arrow);
    }

    $('.show_reply').removeClass('show_reply');
    parent.addClass('show_reply');

    parent.find('textarea').focus();
}

function diskursNewPost(e) {
    var form = $(this);
    var postData = form.serializeArray();
    if (form.parent().parent().prev().prev('.arrow_wrapper').data('last_id')) {
        postData[postData.length] = { name: "last_id", value: form.parent().parent().prev().prev('.arrow_wrapper').data('last_id') };
    }
    var formURL = form.attr('action');
    $.ajax({
        url : formURL,
        type: "POST",
        data : postData,
        success:function(data, textStatus, jqXHR)
        {
            if (data.success) {
                form.parent().before(data.posts);
                form.parent().parent().parent().addClass('has_children');
                var count = parseInt(form.parent().parent().children('.post').length);
                form.parent().parent().parent().children('.container').children('.post_header').children('.count').html(count);
                form.parent().prev().children('.container').children('.post_content').readmore({
					speed: 75,
					collapsedHeight: 200,
					heightMargin: 32,
                    lessLink: '<a class="read_less" href="#">Shrink</a>',
                    moreLink: '<a class="read_more" href="#">Show all</a>'
                });
                form.parent().parent().prev().prev('.arrow_wrapper').data('last_id', data.new_last_id);
                form.find('textarea').val('');
                form.parent().parent().parent().removeClass('show_reply');

                Gifffer();

                refreshNew();
            } else {
                alert(data.message);
            }
        },
    });
    e.preventDefault();
}

function diskursShowPost(element) {
    var parent = element.parent();

    //if the element is already visible, we just have to hide the child postings if neccessary
    if (parent.hasClass('show_child')) {
        if (parent.children('.child_post').children('.show_child').length > 0) {
            var elementToFadeOut = parent.children('.child_post').children('.show_child');

            elementToFadeOut.children('.child_post').fadeOut('slow', function() {
                elementToFadeOut.removeClass('show_child');
                $(this).css('display', '');
                resizeCanvas(true);
            });
        }

    } else {
        var elementToFadeIn = parent;

        //check if parent posts of post to display are visible
        parent.parents('.post').each(function() {
            var current = $(this);

            if (current.hasClass('show_child')) {
                return false;
            } else {
                elementToFadeIn.addClass('show_child');
                elementToFadeIn = current;
            }
        });


        if (elementToFadeIn.siblings('.show_child').length > 0) {
            var elementToFadeOut = $(elementToFadeIn.siblings('.show_child')[0]);
            elementToFadeOut.children('.child_post').fadeOut('slow', function() {
                elementToFadeOut.removeClass('show_child');
                elementToFadeOut.find('.show_child').removeClass('show_child');
                $(this).css('display', '');

                elementToFadeIn.addClass('show_child');
                elementToFadeIn.children('.child_post').fadeIn('slow', function() {
                    $(this).css('display', '');
                    resizeCanvas(true);
                });
            });
        } else {
            elementToFadeIn.addClass('show_child');
            elementToFadeIn.children('.child_post').fadeIn('slow', function() {
                $(this).css('display', '');
                resizeCanvas(true);
            });
        }
    }

    parent.addClass('in_progress');

    url = element.attr('href');

    $.ajax({
        url: url + 'ajax/',
        data: { 'last_id': $(element).data('last_id')},
        success:function(data, textStatus, jqXHR)
            {
                if (data.success) {
                    if (data.new_last_id) {
                        $(element).next().next('.child_post').children('.post_reply').before(data.posts);

                        var count = parseInt($(element).next().next('.child_post').children('.post').length);
                        parent.children('.container').children('.post_header').children('.count').html(count);

                        $(element).data('last_id', data.new_last_id);
                        parent.addClass('has_children');

                        Gifffer();

                        refreshNew();
                    }
                } else {
                    alert(data.message);
                }
                parent.removeClass('in_progress');
            },
    });
}

function diskursHidePost(element) {
    element.parent().children('.child_post').fadeOut('slow', function() {
        element.parent().removeClass('show_child');
        element.parent().find('.show_child').removeClass('show_child');
        $(this).css('display', '');

        resizeCanvas(true);
    });
}

function isPicURL(url) {
    return(url.match(/^http.+\.(jpeg|jpg|gif|png|tiff|bmp)$/) != null);
}

function isURL(url) {
    return(url.match(/^http/) != null);
}

$(document).ready(function() {
    $('#diskurs').on('click', 'a.arrow_wrapper', function() {
        if ($(this).parent().hasClass('show_child') && $(this).parent().hasClass('has_children') && !$(this).parent().hasClass('level0')) {
            diskursHidePost($(this));
            var prev = $(this).parent().parent().prev().prev();
            history.pushState({post: '#'+prev.attr('id')}, '', prev.attr('href'));
        } else {
            diskursShowPost($(this));
            if (history.state == null || history.state.post != '#'+$(this).attr('id')) {
                history.pushState({post: '#'+$(this).attr('id')}, '', $(this).attr('href'));
            }
            /*
			var scrolVal = $(this).offset().left + $( document ).scrollLeft() + 400 - $( window ).width();
			$('body').animate({scrollLeft:scrolVal},500);
			$(this).next().hide();
			*/
        }
        return false;
    });
    $('#diskurs').on('click', '.reply', diskursReply);
    $('#diskurs').on('submit', 'form', diskursNewPost);
    $('.post_content').readmore({
        speed: 75,
		collapsedHeight: 200,
		heightMargin: 32,
		lessLink: '<a class="read_less" href="#"><i class="fa fa fa-angle-double-up"></i></a>',
        moreLink: '<a class="read_more" href="#"><i class="fa fa-angle-double-down"></i></a>'
    });

    $('#diskurs').on('click', '.toggle_emojipicker', function() {

        $(this).prev().prev().prev().prev().emojiPicker({
            width: '300px',
            height: '200px',
            button: false
        });

        $(this).prev().prev().prev().prev().emojiPicker('toggle');
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

    refreshNew();
});

window.onpopstate = function(event) {
    if (event.state != null) {
        diskursShowPost($(event.state.post));
    } else {
        $('#diskurs').find('.show_child').each(function() {
            var el = $(this);
            $(this).children('.child_post').fadeOut('slow', function() {
               el.removeClass('show_child');
            });
        })
    }
};

window.onload = function() {
  Gifffer();
}

function refreshNew() {
    $('div.post').each(function () {
        var newCount = $(this).find('.child_post .new_post').length;

        if (newCount > 0) {
            $(this).children('.new_count').html(newCount);
			$(this).children('.new_count').show();
        } else {
            $(this).children('.new_count').html('');
			$(this).children('.new_count').hide();
        }
    });
}

function resizeCanvas(scroll) {
    var width = $(window).width();
    var height = $(window).height();
    var maxLeft = 0;
    var minLeft = 0;


    var maxWidth=0;
    var minWidth=0;
    var maxHeight=0;
    var minHeight=0;
    $('.show_child > .child_post').each(function() {
        var currentMinWidth = $(this).offset().left;
        var currentMinHeight = $(this).offset().top;
        var currentMaxWidth = currentMinWidth + $(this).width();
        var currentMaxHeight = currentMinHeight + $(this).height();

        if (minWidth < currentMinWidth) {
            minWidth = currentMinWidth
        }
        if (minHeight < currentMinHeight) {
            minHeight = currentMinHeight;
        }
        if (maxWidth < currentMaxWidth) {
            maxWidth = currentMaxWidth
        }
        if (maxHeight < currentMaxHeight) {
            maxHeight = currentMaxHeight;
        }
    });

    var scrollMaxLeft = maxWidth - width;
    var scrollMaxTop = maxHeight - height;
    var currentScrollLeft = $('html, body').scrollLeft();

    if (currentScrollLeft < scrollMaxLeft || currentScrollLeft > scrollMaxLeft) {
        var scrollTop = $('html, body').scrollTop();

        if (scrollTop > scrollMaxTop) {
            scrollTop = scrollMaxTop;
        }

        $('html, body').animate({scrollLeft: scrollMaxLeft, scrollTop: scrollTop}, 'slow', 'swing', function() {
            $('#diskurs').width(maxWidth);
            $('#diskurs').height(maxHeight);
        });
    }
}