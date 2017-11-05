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
          <Route path={`${base_path}`}
                 component={Kanban} />
        </div>
        <Modal returnTo={`${base_path}`} course={props.course}>
          <Switch>
            <Route exact path={`${base_path}issue/add`}
                   component={IssueFormContainer} />
            <Route exact path={`${base_path}issue/:id`}
                   component={IssueContainer} />
          </Switch>
        </Modal>
      </div>
    </BrowserRouter>
  );
};