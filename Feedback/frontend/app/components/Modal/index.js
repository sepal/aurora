import React from 'react';
import {Link} from 'react-router';
import styles from './style.scss';

export default class Modal extends React.Component {
  constructor(props) {
    super(props)

    this.close = this.close.bind(this);
  }

  render() {
    return (
      <div className={styles.modal} onClick={this.close}>
        <div className={styles.window} onClick={this.eventHandler}>
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

  close(event) {
    this.props.onClose();
  }

  eventHandler(event) {
    event.stopPropagation();
  }
}
