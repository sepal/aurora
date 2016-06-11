import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import LaneList from '../LaneList';

class Feedback extends React.Component {
  render() {
    return (
      <div styleName="feedback">
        <LaneList />
      </div>
    );
  }
}

export default CSSModules(Feedback, styles)
