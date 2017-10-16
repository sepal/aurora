import PropTypes from 'prop-types';
import React from 'react';

import InputElement from '../InputElement';

export default class Select extends InputElement {
  static propTypes = {
    name: PropTypes.string,
    label: PropTypes.string,
    options: PropTypes.object,
    value: PropTypes.string,
    onChange: PropTypes.func
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
      <div className="select">
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