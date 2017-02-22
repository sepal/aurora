import React from 'react';
import styles from './style.scss';
import {IssueTypes} from '../../../constants';

export default class IssueLabel extends React.Component {
  static propTypes = {
    type: React.PropTypes.string.isRequired,
    title: React.PropTypes.string.isRequired,
    onChange: React.PropTypes.func,
  };

  static defaultProps = {
    onChange: (type, title) => {}
  };

  constructor(props) {
    super(props);

    this.onLabelClick = this.onLabelClick.bind(this);
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
    let label = '';
    switch (this.props.type) {
      case 'bug':
        label = 'Bug';
        break;
      case 'feature_request':
        label = 'Feature Request';
        break;
      case 'feedback':
        label = 'Feedback';
        break;
      case 'security':
        label = 'Security';
        break;
    }


    if (this.state.editing === true) {
      const options = IssueTypes.map((type) => (
          <option key={type.key} value={type.key}>{type.label}</option>
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
      <div onClick={this.onLabelClick}>
        <span
          className={styles.issueTypeLabel}>[{label}]</span> {this.props.title}
      </div>
    );
  }

  save() {
    this.props.onChange(this.state.type, this.state.title);
    this.closeEditing();
  }

  onBlur(event) {
    if (this.state.editing == true) {
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

  onLabelClick(event) {
    if (!this.editing) {
      const newState = Object.assign(this.state, {'editing': true});
      this.setState(newState);
    }
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