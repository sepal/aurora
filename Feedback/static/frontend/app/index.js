import React from 'react';
import ReactDOM from 'react-dom';
import Feedback from './components/Feedback';

document.addEventListener("DOMContentLoaded", function(event) {
  var node = document.getElementById('test');
  ReactDOM.render(<Feedback />, node);
});
