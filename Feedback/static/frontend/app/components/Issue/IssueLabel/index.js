import React from 'react';
import styles from './style.scss';
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
    this.onBlur = this.onBlur.bind(this);

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
        <div className={styles.issueTypeLabel} onBlur={this.onBlur}>
          <span className={styles.issueTypeLabel}>
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
        <span
          className={styles.issueTypeLabel}>[{label}]</span> {this.props.title}
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

  onBlur(event) {
    if (this.state.editing === true && !this.editing) {
      // todo: currently also called when switching to inner element, therefore
      // deactivated.
      //const newState = Object.assign(this.state, {'editing': false});
      //this.setState(newState);
    }
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