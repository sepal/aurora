import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import Lane from '../Lane';

function LaneList(props) {
  var lanes = props.lanes.map(lane => {
    return (
      <li styleName="item" key={lane.id}>
        <Lane title={lane.name} />
      </li>
    )
  });
  return (
    <ul styleName='laneList'>
      {lanes}
    </ul>
  );
}

export default CSSModules(LaneList, styles)
