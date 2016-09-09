import React from 'react';
import styles from './style.scss';

import Lane from '../Lane';

export default function LaneList(props) {
  var lanes = props.lanes.map(lane => {
    return (
      <li className={styles.item} key={lane.id}>
        <Lane {...lane} />
      </li>
    )
  });
  return (
    <ul className={styles.laneList}>
      {lanes}
    </ul>
  );
}
