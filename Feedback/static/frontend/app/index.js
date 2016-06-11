import React from 'react';
import ReactDOM from 'react-dom';
import Hello from './hello';

document.addEventListener("DOMContentLoaded", function(event) {
  var node = document.getElementById('test');
  ReactDOM.render(<Hello name="John" />, node);
});
