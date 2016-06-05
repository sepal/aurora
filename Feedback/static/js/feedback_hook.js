$(function () {
  $("#bugs-li a").click(function ( event ) {
    event.preventDefault();

    $.ajax({
      url: "/gsi/feedback/new",
      cache: false,
      success: function (html) {
        $('body').append(html);
      }
    });
  });
});