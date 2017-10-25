import PropTypes from 'prop-types';
import React from 'react';

export default class InputElement extends React.Component {
  static propTypes = {
    label: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    error: PropTypes.string,
    onChange: PropTypes.func
  };

  static defaultProps = {
    error: '',
    onChange: () => {}
  };

  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
  }

  renderErrorMsg() {
    if (!this.props.error || this.props.error == '') {
      return (<div></div>);
    }

    return (
      <div className="input--error">
        {this.props.error}
      </div>
    )
  }

  onChange(event) {
    this.props.onChange(event.target.name, event.target.value);
  }
}