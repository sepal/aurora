import React from 'react';
import {observer} from 'mobx-react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';
import kanbanStore from '../../models/kanbanStore';
import DevTools from 'mobx-react-devtools';

import {LaneList} from '../Lanes';

@observer
class Feedback extends React.Component {
  render() {
    return (
      <div styleName="kanban">
        <button styleName="add">
          <i className="fa fa-plus"></i> Add a new issue
        </button>
        <LaneList lanes={kanbanStore.lanes} />
        <DevTools />
      </div>
    );
  }
}

export default CSSModules(Feedback, styles)
