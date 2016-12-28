import React from 'react';
import {observer} from 'mobx-react';
import DevTools from 'mobx-react-devtools';
import {Link} from 'react-router';
import { DragDropContext } from 'react-dnd';
import HTML5Backend from 'react-dnd-html5-backend';

import {LaneList} from '../Lanes';
import kanbanStore from '../../models/kanbanStore';

import styles from './style.scss';

@observer
@DragDropContext(HTML5Backend)
export default class Feedback extends React.Component {
  render() {
    return (
      <div className={styles.kanban}>
        <Link to="/gsi/feedback/issue/add" className={styles.add}>
          <i className="fa fa-plus"></i> Add a new issue
        </Link>
        <LaneList lanes={kanbanStore.lanes} />
        <DevTools />
      </div>
    );
  }
}
