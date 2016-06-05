"use strict";

$(function () {
  $("#bugs-li a").click(function ( event ) {
    event.preventDefault();

    $.ajax({
      url: "/gsi/feedback/post_form",
      cache: false,
      success: function (html) {
        $('body').append(html);
      }
    });
  });

  var feedback_location = window.location.href.split('#')[1];

  if (feedback_location) {
    feedback_location = feedback_location.split('/');
    console.log(feedback_location);

    if (feedback_location && feedback_location[0] == 'feedback') {
      $.ajax({
        url: "/gsi/feedback/success?message=" + feedback_location[1],
        cache: false,
        success: function (html) {
          $('body').append(html);
        }
      });
    }
  }
});