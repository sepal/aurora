import React from 'react';
import {Link} from 'react-router-dom';
import {DragDropContext} from 'react-dnd';
import HTML5Backend from 'react-dnd-html5-backend';

import {LaneListContainer} from '../../containers';

@DragDropContext(HTML5Backend)
export default class Kanban extends React.Component {
  componentDidMount() {
    kanbanReady();
  }
  render() {
    return (
      <div className="kanban">
        <div className="kanban__add">
          <Link to={`${base_path}issue/add`}>
            Add issue
          </Link>
        </div>
        <LaneListContainer />
      </div>
    );
  }
}
