import React from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import Kanban from '../Kanban';
import {IssueContainer, IssueFormContainer} from '../../containers'
import Modal from '../Modal';

const add = () => (
  <div>Add issue</div>
);
const edit = () => (
  <div>Edit issue</div>
);

export default function (props) {
  return (
    <BrowserRouter>
      <div>
        <div className="content">
          <Route path={`/${props.course}/feedback`}
                 component={Kanban} />
        </div>
        <Modal returnTo={`/${props.course}/feedback`} course={props.course}>
          <Switch>
            <Route exact path={`/${props.course}/feedback/issue/add`}
                   component={IssueFormContainer} />
            <Route exact path={`/${props.course}/feedback/issue/:id`}
                   component={IssueContainer} />
          </Switch>
        </Modal>
      </div>
    </BrowserRouter>
  );
};