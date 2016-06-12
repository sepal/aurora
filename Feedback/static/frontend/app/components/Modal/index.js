import React from 'react';
import {Link} from 'react-router';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

class Modal extends React.Component {
  render() {
    return (
      <div styleName='modal'>
        <div styleName="window">
          <div styleName="header">
            <Link to={this.props.returnTo}>
              <button styleName="close">
                <i className="fa fa-times-circle"></i>
              </button>
            </Link>
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
