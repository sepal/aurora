import React from 'react';
import styles from './style.scss';

import InputElement from '../InputElement';

export default class Select extends InputElement {
  static propTypes = {
    name: React.PropTypes.string,
    label: React.PropTypes.string,
    options: React.PropTypes.object,
    value: React.PropTypes.string,
    onChange: React.PropTypes.func
  };

  static defaultProps = {
    onChange: (event) => {
    }
  };

  render() {
    const options = Object.keys(this.props.options).map((key) => (
      <option key={key} value={key}>{this.props.options[key]}</option>
    ));

    return (
      <div className={styles.select}>
        <label htmlFor={this.props.name}>{this.props.label}:</label>
        <select name={this.props.name} id={this.props.name}
                defaultValue={this.props.value}
                onChange={this.onChange}>
          {options}
        </select>
      </div>
    );
  }
}