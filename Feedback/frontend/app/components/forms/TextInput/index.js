import PropTypes from 'prop-types';
import React from 'react';

import InputElement from '../InputElement';

export default class TextInput extends InputElement {
  static propTypes = {
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    size: PropTypes.number,
    onChange: PropTypes.func
  };

  static defaultProps = {
    size: 64,
    onChange: (event) => {
    }
  };

  render() {
    const classNames = this.props.error == '' ? 'textinput'
      : 'textinput textinput--error';
    return (
      <div className={classNames}>
        <label htmlFor={this.props.name}>{this.props.label}:</label>
        <input type="text"
               id={this.props.name}
               name={this.props.name}
               value={this.props.value}
               size={this.props.size}
               onChange={this.onChange} />
        {this.renderErrorMsg()}
      </div>
    );
  }
}