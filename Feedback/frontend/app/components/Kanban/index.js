import React from 'react';
import {Link} from 'react-router';
import {DragDropContext} from 'react-dnd';
import HTML5Backend from 'react-dnd-html5-backend';

import {LaneListContainer} from '../../containers';

import styles from './style.scss';

@DragDropContext(HTML5Backend)
export default class Feedback extends React.Component {
  render() {
    return (
      <div className={styles.kanban}>
        <div className={styles.add}>
          <Link to={`/${course_short_title}/feedback/issue/add`}>
            <i className="fa fa-plus"></i> Add a new issue
          </Link>
        </div>
        <LaneListContainer />
      </div>
    );
  }
}
