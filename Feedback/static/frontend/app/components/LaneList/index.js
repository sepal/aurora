import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import Lane from '../Lane';

function LaneList(props) {
  return (
    <ul styleName='laneList'>
      <li styleName="item">
        <Lane title="New"/>
      </li>
      <li styleName="item">
        <Lane title="InProgress"/>
      </li>
      <li styleName="item">
        <Lane title="Finished"/>
      </li>
    </ul>
  );
}

export default CSSModules(LaneList, styles)
