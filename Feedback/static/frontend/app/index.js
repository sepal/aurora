import Moment from 'moment';
import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, IndexRoute, browserHistory} from 'react-router';
import kanbanStore from './models/kanbanStore';

import Feedback from './components/Feedback';
import Kanban from './components/Kanban';
import {IssueDetail, IssueForm} from './components/Issue';


document.addEventListener("DOMContentLoaded", function (event) {
  Moment.locale('en');

  let str = document.getElementById('data').innerHTML;
  kanbanStore.loadFromJSONString(str);

  var node = document.getElementById('test');
  ReactDOM.render(
    (
      <Router history={browserHistory}>
        <Route path="/gsi/feedback" component={Feedback}>
          <IndexRoute component={Kanban} />
          <Route path="/gsi/feedback/issue/:id" component={IssueDetail} />
          <Route path="/gsi/feedback/issue/:id/edit" component={IssueForm} />
        </Route>
      </Router>
    ), node);
});

