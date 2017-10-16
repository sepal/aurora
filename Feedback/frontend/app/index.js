import Moment from 'moment';
import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import {BrowserRouter} from 'react-router';

import Routing from './components/Routing';
import configureStore from './store';

document.addEventListener("DOMContentLoaded", function (event) {
  Moment.locale('en');

  let data = {};
  try {
    data = JSON.parse(initial_data);
  } catch ($exception) {
    console.error($exception);
  }

  const store = configureStore(data);

  var node = document.getElementById('app-root');
  ReactDOM.render(
    (
      <Provider store={store}>
        <Routing course={course_short_title} />
      </Provider>
    ), node);
});

