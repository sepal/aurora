import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import LaneList from '../LaneList';

class Feedback extends React.Component {
  render() {
    return (
      <div styleName="kanban">
        <button styleName="add">
          <i className="fa fa-plus"></i> Add a new issue
        </button>
        <LaneList lanes={lane_list} />
      </div>
    );
  }
}

export default CSSModules(Feedback, styles)
