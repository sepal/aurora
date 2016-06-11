import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import LaneList from '../LaneList';

import LanesMockup from '../../mockup/lanes';

class Feedback extends React.Component {
  render() {
    return (
      <div styleName="feedback">
        <LaneList lanes={LanesMockup} />
      </div>
    );
  }
}

export default CSSModules(Feedback, styles)
