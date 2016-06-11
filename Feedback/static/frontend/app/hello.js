import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './hello.scss';

class Hello extends React.Component {
  render() {
    return (
      <div styleName='box'>
        Hello, {this.props.name}!
      </div>
    );
  }
}

export default Hello;