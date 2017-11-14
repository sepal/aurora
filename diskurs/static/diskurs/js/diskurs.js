$(document).ready(function() {
    $('#diskurs-li').addClass('uRhere');
})



var quotePost = "";
var quotePostMarkdown = "";
var scrollingEnabled = true;
var lastPostId = 0;

function diskursReply() {
    var parent = $(this).parent().parent().parent();
    var arrow = parent.children('.arrow_wrapper').first();

    if (history.state == null || history.state.post != '#'+$(arrow).attr('id')) {
        history.pushState({post: '#'+$(arrow).attr('id')}, '', $(arrow).attr('href'));
    }

    $('.show_reply').removeClass('show_reply');
    $('.post_preview').html('');
    parent.addClass('show_reply');

    parent.children('.child_post').children('.post_reply').find('.reply_area').emojiPicker({
        width: '300px',
        height: '200px',
        button: false
    });

    if (!parent.hasClass('show_child')) {
        diskursShowPost(arrow, true);
    } else {
        resizeCanvas(true);
    }
}

function diskursNewPost(e) {
    var form = $(this);
    var postData = form.serializeArray();
    postData[postData.length] = { name: "last_id", value: lastPostId };
    var formURL = form.attr('action');
    $.ajax({
        url : formURL,
        type: "POST",
        data : postData,
        success:function(data, textStatus, jqXHR)
        {
            if (data.success) {
                if (data.return_object) {

                    for (var post_id in data.return_object) {
                        $(data.return_object[post_id]).insertBefore('#post-' + post_id + ' > .child_post > .post_reply');
                        $('#post-' + post_id).addClass('has_children');
                    }

                    setLatestPostIdAndRecount();
                    decoratePosts();

                    form.find('textarea').val('');
                    form.parent().parent().parent().parent().removeClass('show_reply');

                    Gifffer();

                    markPostingsAsSeen();
                }
            } else {
                alert(data.message);
            }
        },
    });
    e.preventDefault();
}

function diskursShowPost(element, scrollToReply) {
    var parent = element.parent();
    var fadeOutDone = false;
    var ajaxRefreshDone = false;

    //if the element is already visible, we just have to hide the child postings if neccessary
    if (parent.hasClass('show_child')) {
        if (parent.children('.child_post').children('.show_child').length > 0) {
            var elementToFadeOut = parent.children('.child_post').children('.show_child');

            elementToFadeOut.children('.child_post').fadeOut('fast', function() {
                elementToFadeOut.removeClass('show_child');
                $(this).css('display', '');

                fadeOutDone = true;
                if (fadeOutDone && ajaxRefreshDone) {
                    markPostingsAsSeen();
                    resizeCanvas(scrollToReply);
                }
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
            elementToFadeOut.children('.child_post').fadeOut('fast', function() {
                elementToFadeOut.removeClass('show_child');
                elementToFadeOut.find('.show_child').removeClass('show_child');
                $(this).css('display', '');

                elementToFadeIn.addClass('show_child');
                elementToFadeIn.children('.child_post').fadeIn('fast', function() {
                    $(this).css('display', '');

                    fadeOutDone = true;
                    if (fadeOutDone && ajaxRefreshDone) {
                        markPostingsAsSeen();
                        resizeCanvas(scrollToReply);
                    }
                });
            });
        } else {
            elementToFadeIn.addClass('show_child');
            elementToFadeIn.children('.child_post').fadeIn('fast', function() {
                $(this).css('display', '');

                fadeOutDone = true;
                if (fadeOutDone && ajaxRefreshDone) {
                    markPostingsAsSeen();
                    resizeCanvas(scrollToReply);
                }
            });
        }
    }

    parent.addClass('in_progress');

    url = element.attr('href');

    $.ajax({
        url: url + 'ajax/',
        data: { 'last_id': lastPostId},
        success:function(data, textStatus, jqXHR)
            {
                if (data.success) {
                    if (data.return_object) {

                        for (var post_id in data.return_object) {
                            $(data.return_object[post_id]).insertBefore('#post-'+post_id+' > .child_post > .post_reply');
                            $('#post-'+post_id).addClass('has_children');
                        }

                        setLatestPostIdAndRecount();
                        decoratePosts();
                        Gifffer();
                    }

                    ajaxRefreshDone = true;
                    if (fadeOutDone && ajaxRefreshDone) {
                        markPostingsAsSeen();
                        resizeCanvas(scrollToReply);
                    }
                } else {
                    alert(data.message);
                }
                parent.removeClass('in_progress');
            },
    });
}

function diskursHidePost(element) {
    element.parent().children('.child_post').fadeOut('fast', function() {
        element.parent().removeClass('show_child');
        element.parent().find('.show_child').removeClass('show_child');
        $(this).css('display', '');

        resizeCanvas(false);
    });
}

function isPicURL(url) {
    return(url.match(/^http.+\.(jpeg|jpg|gif|png|tiff|bmp)$/) != null);
}

function isURL(url) {
    return(url.match(/^http/) != null);
}

$(document).ready(function() {
    decoratePosts();
    $('#diskurs').on('click', 'a.arrow_wrapper', function() {
        if ($(this).parent().hasClass('show_child') && !$(this).parent().hasClass('level0')) {
            diskursHidePost($(this));
            var prev = $(this).parent().parent().prev().prev();
            history.pushState({post: '#'+prev.attr('id')}, '', prev.attr('href'));
        } else {
            diskursShowPost($(this), false);
            if (history.state == null || history.state.post != '#'+$(this).attr('id')) {
                history.pushState({post: '#'+$(this).attr('id')}, '', $(this).attr('href'));
            }
        }
        return false;
    });
    $('#diskurs').on('click', 'a.new_count', function() {

        var next_new_id = $(this).data('next_new_id');
        var $arrow_element = $("#" + next_new_id);

        diskursShowPost($arrow_element, false);
        if (history.state == null || history.state.post != '#'+next_new_id) {
            history.pushState({post: '#'+next_new_id}, '', $arrow_element.attr('href'));
        }
        return false;
    });
    $('#diskurs').on('click', '.reply', diskursReply);
    $('#diskurs').on('submit', 'form', diskursNewPost);
    $('#diskurs').on('click', '.cancel_reply', function() {
        var $child_post = $(this).parent().parent().parent().parent();
        $child_post.parent().removeClass('show_reply');
    });
    $('#diskurs').on('click', '.preview_reply', function() {
        var preview_content = $(this).parent().children('textarea').val();
        var csfr = $(this).parent().children('input[name="csrfmiddlewaretoken"]').val();
        var $contentDiv = $(this).parent().prev();

        $.ajax({
            url: diskurs_preview_url,
            method: "POST",
            data: {content : preview_content, csrfmiddlewaretoken : csfr},
            success:function(data, textStatus, jqXHR)
                {
                    if (data.success) {
                        $contentDiv.html(data.content);
                        Gifffer();
						$('.post_button').removeClass('not_here_first');
                    } else {
                        alert(data.message);
                    }
                },
        });
    });

    $('#diskurs').on('click', '.toggle_emojipicker', function() {
        $(this).parent().children('.reply_area').emojiPicker('toggle');
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
        quotePostMarkdown = $(this).parent().find('.user').text() + ' wrote:\n' + '> ' + quotePost.replace('\n', '\n> ') + '\n\n';
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

    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        scrollingEnabled = false;
    }

    markPostingsAsSeen();
    setLatestPostIdAndRecount();
});

window.onpopstate = function(event) {
    if (event.state != null) {
        diskursShowPost($(event.state.post), false);
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

            var next_new_post = $(this).find('.child_post .new_post').first().parent().parent().parent().children('.arrow_wrapper').first().attr('id');
            var $new_count_el = $(this).children('.new_count').first();

            $new_count_el.data('next_new_id', next_new_post);
        } else {
            $(this).children('.new_count').html('');
			$(this).children('.new_count').hide();
        }
    });
}

function resizeCanvas(scrollToReply) {
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

    var scrollMinTopCorrection = 100;
    var scrollMaxLeft = maxWidth - width + 50; //50 px padding
    var scrollMaxTop = maxHeight - height + 150; //150 px padding
    var scrollMinTop = minHeight + scrollMinTopCorrection - height;
    var currentScrollLeft = $(document).scrollLeft();

    var currentScrollTop = $(document).scrollTop();
    var scrollTop = currentScrollTop;

    var postReplyElement = false;
    if (scrollToReply) {
        var $postReplyElement = $('.post_reply:visible');

        //scroll 150 px more so that the emojis widget is completely visible
        var scrollMinReplyCorrection = 150;

        var scrollMinReply = $postReplyElement.offset().top + $postReplyElement.height() + scrollMinReplyCorrection - height;
        var scrollMaxReply = $postReplyElement.parent().offset().top - $('.diskurs_head').height();

        if (scrollMinReply > scrollTop) {
            scrollTop = scrollMinReply;
        } else if (scrollMaxReply < scrollTop) {
            scrollTop = scrollMaxReply
        }


    } else if (scrollTop < scrollMinTop) {
        scrollTop = scrollMinTop;
    }

    if (scrollTop > scrollMaxTop) {
        scrollTop = scrollMaxTop;
    }

    if (scrollingEnabled &&
        (currentScrollLeft < scrollMaxLeft || currentScrollLeft > scrollMaxLeft)) {

        $('html, body').animate({scrollLeft: scrollMaxLeft, scrollTop: scrollTop}, 'slow', 'swing', function() {
            $('#diskurs').width(maxWidth);
            $('#diskurs').height(maxHeight);

            if (scrollToReply) {
                $postReplyElement.find('textarea').focus();
            }
        });

    } else if (scrollingEnabled && currentScrollTop != scrollTop) {

        $('html, body').animate({scrollTop: scrollTop}, 'slow', 'swing', function() {
            $('#diskurs').width(maxWidth);
            $('#diskurs').height(maxHeight);

            if (scrollToReply) {
                $postReplyElement.find('textarea').focus();
            }
        });

    } else {
        $('#diskurs').width(maxWidth);
        $('#diskurs').height(maxHeight);

        if (scrollToReply) {
            $postReplyElement.find('textarea').focus();
        }
    }
}

function markPostingsAsSeen() {
    $('#diskurs').find('.new_post').filter(":visible").each(function() {
        $(this).addClass('seen_post').removeClass('new_post');
    });
    $('.level1 .post_content:not([aria-expanded])').readmore({
        speed: 75,
		collapsedHeight: 200,
		heightMargin: 32,
		lessLink: '<a class="read_less" href="#"><i class="fa fa fa-angle-double-up"></i></a>',
        moreLink: '<a class="read_more" href="#"><i class="fa fa-angle-double-down"></i></a>'
    });
    refreshNew();
}

function setLatestPostIdAndRecount() {
    $('#diskurs').find('.post').each(function() {
        var currentPostId = parseInt($(this).attr('id').substr(5));
        if (currentPostId > lastPostId) {
            lastPostId = currentPostId;
        }
        var childCount = $(this).find('.post').length;
        if (childCount > 0) {
            $(this).children('.container').children('.post_header').children('.count').html(childCount);
        } else {
            $(this).children('.container').children('.post_header').children('.count').html('');
        }
    })
}

function decoratePosts() {
    $('#diskurs').find('.nolevel').each(function() {
        $(this).removeClass('nolevel');
        $(this).addClass('level'+$(this).parents('.post').length);
    })
}