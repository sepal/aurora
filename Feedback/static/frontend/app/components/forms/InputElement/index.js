import React from 'react';

export default class InputElement extends React.Component {
  static propTypes = {
    label: React.PropTypes.string.isRequired(),
    name: React.PropTypes.string.isRequired(),
    value: React.PropTypes.string.isRequired(),
    onChange: React.PropTypes.func
  };

  static defaultProps = {
    onChange: () => {}
  };

  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
  }

  onChange(event) {
    this.props.onChange(event.target.name, event.target.value);
  }
}