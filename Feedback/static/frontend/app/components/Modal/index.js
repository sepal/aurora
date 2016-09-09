import React from 'react';
import {Link} from 'react-router';
import styles from './style.scss';

export default class Modal extends React.Component {
  render() {
    return (
      <div className={styles.modal}>
        <div className={styles.window}>
          <div className={styles.header}>
            <Link to={this.props.returnTo}>
              <button className={styles.close}>
                <i className="fa fa-times-circle"></i>
              </button>
            </Link>
          </div>
          <div>
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }
}
