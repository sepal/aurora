import React from 'react';
import {Link} from 'react-router';
import {DragDropContext} from 'react-dnd';
import HTML5Backend from 'react-dnd-html5-backend';

import {LaneListContainer} from '../../containers';

@DragDropContext(HTML5Backend)
export default class Feedback extends React.Component {
  componentDidMount() {
    kanbanReady();
  }
  render() {
    return (
      <div className="kanban">
        <div className="kanban__add">
          <Link to={`/${course_short_title}/feedback/issue/add`}>
            Add issue
          </Link>
        </div>
        <LaneListContainer />
      </div>
    );
  }
}
