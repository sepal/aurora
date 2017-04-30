/**
 * @file
 * This file servers as a hacky way to be able to inject stuff, without to
 * manipulate the front end code.
 */

/**
 * Is called as soon as the mounted
 */
var kanbanReady = function() {
  $('.lane').each(function() {
    $(this).css('background-position-x', (Math.floor(Math.random() * 50) + 50) + '%');
  });
};