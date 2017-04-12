/**
 * @file
 * This file servers as a hacky way to be able to inject stuff, without to
 * manipulate the front end code.
 */

function hashCode(s) {
  return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function markNewItems() {
  var aList = [];
  fCookie = getCookie('issueCookie.{{user.nickname}}');
  if (fCookie == null) fCookie = "";
  iCookie = fCookie.split(',');
  var zhl = 0;
  $('.issue-list__item').each(function() {
    thisCode = hashCode($(this).find('.issue--teaser__body').text() + $(this).find('.issue--teaser__footer').text()) + "";
    if ($.inArray(thisCode, iCookie) == -1) {
      $(this).addClass('markChanged');
      zhl++;
    }
    aList[aList.length] = thisCode;
  });
  document.cookie = 'issueCookie.{{user.nickname}}= ' + aList + "; expires=Tue, 18 Jan 2038 03:14:06 GMT";
  if (zhl == 1) {
    $('.kanban__add').append('<div class="changedIssues"> one change</div>');
  } else if (zhl > 1) {
    $('.kanban__add').append('<div class="changedIssues"> ' + zhl + ' changes</div>');
  } else {
    $('.kanban__add').append('<div class="noChangedIssues"> no changes</div>');
  }
}

/**
 * Is called as soon as the mounted
 */
var kanbanReady = function() {
  $('.lane').each(function() {
    $(this).css('background-position-x', (Math.floor(Math.random() * 50) + 50) + '%');
  });

  $('.issue__type-label').each(function() {
    if ($(this).text() == "[Bug]")  {
      $(this).html("<i class='fa fa-bug'></i>");
    } else if ($(this).text() == "[Feature Request]")  {
      $(this).html("<i class='fa fa-lightbulb-o'></i>");
    } else if ($(this).text() == "[Feedback]")  {
      $(this).html("<i class='fa fa-commenting-o'></i>");
    } else if ($(this).text() == "[Security]")  {
      $(this).html("<i class='fa fa-lock'></i>");
    }
  });
  $('.lane').last().find('.issue-list__item').addClass('headOnly');
  markNewItems();
};