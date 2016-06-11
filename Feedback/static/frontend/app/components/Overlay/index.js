import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

class Overlay extends React.Component {
  render() {
    return (
      <div styleName='overlay'>
        
      </div>
    );
  }
}

export default CSSModules(Overlay, styles)
