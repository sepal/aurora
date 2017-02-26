import React from 'react';
import styles from './style.scss';
import {withRouter} from 'react-router';

import IssueModel from '../../../models/issue';
import {TextInput, TextArea, Select, Submit} from '../../forms';
import {IssueTypes} from '../../../constants'

class IssueForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      issue: new IssueModel()
    };

    this.updateChange = this.updateChange.bind(this);
    this.handleClick = this.handleClick.bind(this);

    this.state = {
      type: Object.keys(IssueTypes)[0],
      title: '',
      body: '',
      title_error: '',
      body_error: ''
    }
  }

  render() {
    return (
      <div className={styles.issueForm}>
        <form>
          <TextInput label="Title" defaultValue={this.state.title}
                     onChange={this.updateChange} name="title" error={this.state.title_error} />
          <Select label="Issue type" options={IssueTypes}
                  defaultValue={this.state.type}
                  onChange={this.updateChange} name="type" />
          <TextArea label="Description" defaultValue={this.state.body}
                    onChange={this.updateChange} name="body" error={this.state.body_error} />
          <Submit onClick={this.handleClick} />
        </form>
      </div>
    );
  }

  handleClick(event) {
    event.preventDefault();
    let newState = Object.assign(this.state);
    if (this.state.title == '') {
      newState['title_error'] = 'Please enter a title';
    }

    if (this.state.body == '') {
      newState['body_error'] = 'Please describe your issue';
    }

    if (newState['body_error'] == '' && newState['title_error'] == '') {
      this.props.createIssue(this.state.type, this.state.title, this.state.body);
    } else {
      this.setState(newState);
    }
  }

  updateChange(key, value) {
    let newState = Object.assign(this.state, {});
    newState[key] = value;
  }
}

export default withRouter(IssueForm);