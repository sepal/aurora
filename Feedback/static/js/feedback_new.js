"use strict";

$(function () {
  if ($(".feedback form")) {
    var action = $(".feedback form").prop("action");
    action += "?redirect=" + window.location.href + "#feedback";
    $(".feedback form").attr("action", action);
  }

  $(".feedback__close").click(function (event) {
    event.preventDefault();

    $(".feedback").remove();
  });

  $(".feedback__tabs__tab").click(function (event) {
    $(".feedback__tabs__tab").removeClass("feedback__tabs__tab--active");
    $(this).addClass("feedback__tabs__tab--active");
    var value = $(this).attr("data-value");

    $(".feedback__form-element--tabs select").val(value);
  })
});