import React from 'react';
import {Redirect} from 'react-router-dom';

import {TextInput, TextArea, Select, Submit} from '../../forms';
import {IssueTypes} from '../../../constants'

class IssueForm extends React.Component {
  constructor(props) {
    super(props);

    this.updateChange = this.updateChange.bind(this);
    this.handleClick = this.handleClick.bind(this);

    this.state = {
      type: Object.keys(IssueTypes)[0],
      title: '',
      body: '',
      title_error: '',
      body_error: '',
      submitted: false
    }
  }

  render() {
    if (this.state.submitted) {
      return (
        <Redirect to={`${base_path}`}/>
      )
    }

    return (
      <div>
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
    } else {
      newState['title_error'] = '';
    }

    if (this.state.body == '') {
      newState['body_error'] = 'Please describe your issue';
    } else {
      newState['body_error'] = '';
    }

    if (newState['body_error'] == '' && newState['title_error'] == '') {
      this.props.createIssue(this.state.type, this.state.title, this.state.body);
      newState['submitted'] = true;
    }
    this.setState(newState);
  }

  updateChange(key, value) {
    let newState = Object.assign(this.state, {});
    newState[key] = value;
  }
}

export default IssueForm;