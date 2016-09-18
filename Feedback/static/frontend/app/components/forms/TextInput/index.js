import React from 'react';
import styles from './style.scss';

import InputElement from '../InputElement';

export default class TextInput extends InputElement {
  static propTypes = {
    name: React.PropTypes.string.isRequired(),
    label: React.PropTypes.string.isRequired(),
    value: React.PropTypes.string.isRequired(),
    size: React.PropTypes.number,
    onChange: React.PropTypes.func
  }

  static defaultProps = {
    size: 64,
    onChange: (event) => {}
  }

  render() {
    return (
      <div className={styles.text_input}>
        <label htmlFor={this.props.name}>{this.props.label}:</label>
        <input type="text"
               id={this.props.name}
               name={this.props.name}
               value={this.props.value}
               size={this.props.size}
               onChange={this.onChange} />
      </div>
    );
  }
};