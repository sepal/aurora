import React from 'react';
import styles from './style.scss';

import Lane from '../Lane';

export default function LaneList(props) {
  var lanes = props.lanes.map(lane => {
    return (
      <div className={styles.item} key={lane.id}>
        <Lane {...lane} />
      </div>
    )
  });
  return (
    <div className={styles.laneList}>
      {lanes}
    </div>
  );
}
