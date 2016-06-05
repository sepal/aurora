$(function () {
  function appendOverlay(html) {

    $('body').append(html);

    $(".feedback__close").click(function (event) {
      event.preventDefault();

      $(".feedback").remove();
    });
  }


  $("#bugs-li a").click(function ( event ) {
    event.preventDefault();

    $.ajax({
      url: "/gsi/feedback/new",
      cache: false,
      success: appendOverlay
    });
  });
});