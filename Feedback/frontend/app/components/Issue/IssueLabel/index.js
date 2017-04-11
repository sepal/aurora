import React from 'react';
import {IssueTypes} from '../../../constants';

export default class IssueLabel extends React.Component {
  static propTypes = {
    type: React.PropTypes.string.isRequired,
    title: React.PropTypes.string.isRequired,
    editable: React.PropTypes.bool,
    onChange: React.PropTypes.func
  };

  static defaultProps = {
    editable: false,
    onChange: (type, title) => {}
  };

  constructor(props) {
    super(props);

    this.enableEditing = this.enableEditing.bind(this);
    this.onSaveClick = this.onSaveClick.bind(this);
    this.onEnterPress = this.onEnterPress.bind(this);
    this.onTypeChange = this.onTypeChange.bind(this);
    this.onTitleChange = this.onTitleChange.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);


    this.state = {
      editing: false,
      type: props.type,
      title: props.title
    }
  }

  render() {
    const label = IssueTypes[this.props.type];

    if (this.state.editing === true) {
      const options = Object.keys(IssueTypes).map((type) => (
          <option key={type} value={type}>{IssueTypes[type]}</option>
      ));

      return (
        <div className="issue__type-label">
          <span className="issue__type-label">
            <select
              defaultValue={this.props.type}
              onChange={this.onTypeChange}
              onKeyPress={this.onEnterPress}
              onKeyDown={this.onKeyDown}>
              {options}
            </select>
          </span>
          <input
            autoFocus
            onKeyPress={this.onEnterPress}
            onKeyDown={this.onKeyDown}
            onChange={this.onTitleChange}
            type="text"
            name="title"
            defaultValue={this.props.title} />
          <button
            onClick={this.onSaveClick}>
            <i className="fa fa-check"></i> Save
          </button>
        </div>
      );
    }

    return (
      <div onClick={this.enableEditing}>
        {this.props.title}
      </div>
    );
  }

  enableEditing() {
    if (this.props.editable) {
      const newState = Object.assign(this.state, {editing: true});
      this.setState(newState);
    }
  }

  save() {
    this.props.onChange(this.state.type, this.state.title);
    this.closeEditing();
  }

  onTypeChange(event) {
    const newState = Object.assign(this.state, {'type': event.target.value});
    this.setState(newState);
  }

  onTitleChange(event) {
    const newState = Object.assign(this.state, {'title': event.target.value});
    this.setState(newState);
  }

  onEnterPress(event) {
    if (event.key == 'Enter') {
      this.save();
    }
  }

  onKeyDown(event) {
    if (event.key == 'Escape') {
      this.closeEditing();
    }
  }

  onSaveClick(event) {
    this.save();
  }

  closeEditing() {
    const newState = Object.assign(this.state, {'editing': false});
    this.setState(newState);
  }
}