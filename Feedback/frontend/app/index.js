import Moment from 'moment';
import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import {Router, Route, IndexRoute, browserHistory} from 'react-router';

import Feedback from './components/Feedback';
import Kanban from './components/Kanban';
import {IssueContainer, IssueFormContainer} from  './containers'
import configureStore from './store';


document.addEventListener("DOMContentLoaded", function (event) {
  Moment.locale('en');

  let str = document.getElementById('data').innerHTML;
  let data = {};
  try {
    data = JSON.parse(str);
  } catch ($exception) {
    console.error($exception);
  }

  const store = configureStore(data);


  var node = document.getElementById('app-root');
  ReactDOM.render(
    (
      <Provider store={store}>
        <Router history={browserHistory}>
          <Route path={`/${course_short_title}/feedback`} component={Feedback}>
            <IndexRoute component={Kanban} />
            <Route path={`/${course_short_title}/feedback/issue/add`} component={IssueFormContainer} />
            <Route path={`/${course_short_title}/feedback/issue/:id`} component={IssueContainer} />
          </Route>
        </Router>
      </Provider>
    ), node);
});

