import React from 'react';

import Lane from '../Lane';

export default function LaneList(props) {
  var lanes = props.lanes.map(lane => {
    return (
      <div className="lane-list__item" key={lane.id}>
        <Lane {...lane} />
      </div>
    )
  });
  return (
    <div className="lane-list">
      {lanes}
    </div>
  );
}
