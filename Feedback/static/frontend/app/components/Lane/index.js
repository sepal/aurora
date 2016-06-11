import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

class Lane extends React.Component {
  render() {
    return (
      <div styleName='lane'>
        <h2 styleName="title">{this.props.title}</h2>
        <div styleName="content">
          foobar
        </div>
      </div>
    );
  }
}

export default CSSModules(Lane, styles)
