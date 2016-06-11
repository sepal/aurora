import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

class Modal extends React.Component {
  render() {
    return (
      <div styleName='modal'>
        <div styleName="window">
          <div styleName="header">
            <button styleName="close">
              <i className="fa fa-times-circle"></i>
            </button>
          </div>
          <div styleName="content">
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }
}

export default CSSModules(Modal, styles)
