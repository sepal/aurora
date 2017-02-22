import Moment from 'moment';
import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import {Router, Route, IndexRoute, browserHistory} from 'react-router';

import Feedback from './components/Feedback';
import Kanban from './components/Kanban';
import {IssueContainer} from  './containers'
import {IssueForm} from './components/Issue'
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

  var node = document.getElementById('test');
  ReactDOM.render(
    (
      <Provider store={store}>
        <Router history={browserHistory}>
          <Route path="/gsi/feedback" component={Feedback}>
            <IndexRoute component={Kanban} />
            <Route path="/gsi/feedback/issue/add" component={IssueForm} />
            <Route path="/gsi/feedback/issue/:id" component={IssueContainer} />
          </Route>
        </Router>
      </Provider>
    ), node);
});

