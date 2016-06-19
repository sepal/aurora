import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import LaneList from '../LaneList';

class Feedback extends React.Component {
  render() {
    let lanes = [];
    lanes = lane_list.map((lane) => {
      return {
        'id': lane.pk,
        'name': lane.fields.name
      }
    });

    return (
      <div styleName="kanban">
        <button styleName="add">
          <i className="fa fa-plus"></i> Add a new issue
        </button>
        <LaneList lanes={lanes} />
      </div>
    );
  }
}

export default CSSModules(Feedback, styles)
