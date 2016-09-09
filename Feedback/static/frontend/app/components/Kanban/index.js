import React from 'react';
import {observer} from 'mobx-react';
import styles from './style.scss';
import kanbanStore from '../../models/kanbanStore';
import DevTools from 'mobx-react-devtools';

import {LaneList} from '../Lanes';

@observer
export default class Feedback extends React.Component {
  render() {
    return (
      <div className={styles.kanban}>
        <button className={styles.add}>
          <i className="fa fa-plus"></i> Add a new issue
        </button>
        <LaneList lanes={kanbanStore.lanes} />
        <DevTools />
      </div>
    );
  }
}
