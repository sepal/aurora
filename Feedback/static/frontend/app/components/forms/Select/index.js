import React from 'react';
import styles from './style.scss';

import InputElement from '../InputElement';

export default class Select extends InputElement {
  static propTypes = {
    name: React.PropTypes.string,
    label: React.PropTypes.string,
    options: React.PropTypes.array(),
    onChange: React.PropTypes.func
  };

  static defaultProps = {
    onChange: (event) => {}
  };

  render() {
    let options = [];
    for (let key in this.props.options) {
      options.push(<option value={key}>{this.props.options[key]}</option>);
    }

    return (
      <div className={styles.select}>
        <label htmlFor={this.props.name}>{this.props.label}:</label>
        <select name={this.props.name} id={this.props.name} onChange={this.onChange} >
          {options}
        </select>
      </div>
    );
  }
}