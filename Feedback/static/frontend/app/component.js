import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './component.scss';

class HelloWorld extends React.Component {
  render() {
    return (
      <div styleName='box'>
        Hello, {this.props.name}!
      </div>
    );
  }
}

export default CSSModules(HelloWorld, styles);