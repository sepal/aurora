import React from 'react';
import styles from './style.scss';

import InputElement from '../InputElement';

export default class TextArea extends InputElement {
  static propTypes = {
    name: React.PropTypes.string,
    label: React.PropTypes.string,
    rows: React.PropTypes.number,
    onChange: React.PropTypes.func
  };

  static defaultProps = {
    rows: 10,
    onChange: (event) => {}
  };

  render() {
    return (
      <div className={styles.text_area}>
        <label htmlFor={this.props.name}>{this.props.label}:</label>
        <textarea rows={this.props.rows}
                  name={this.props.name}
                  id={this.props.name}
                  onChange={this.onChange}>
        {this.props.value}
      </textarea>
      </div>
    );
  }
};
