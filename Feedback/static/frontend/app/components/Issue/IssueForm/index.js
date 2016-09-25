import React from 'react';
import styles from './style.scss';
import {observer} from 'mobx-react';

import IssueModel from '../../../models/issue';
import {TextInput, TextArea, Select, Submit} from '../../forms';

@observer
class IssueForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      issue: new IssueModel()
    };

    this.updateChange = this.updateChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    if (this.props.params) {
      this.state.issue .loadFromAJAX(this.props.params.id);
    }
  }

  handleClick(event) {
    event.preventDefault();
    this.state.issue .update();
  }

  updateChange(key, value) {
    let state = this.state;
    state.issue [key] = value;
    console.log(state);
    this.setState(state);
  }

  render() {
    return (
      <div className={styles.issueForm}>
        <form>
          <TextInput label="Title" value={this.state.issue.title}
                     onChange={this.updateChange} name="title" />
          <Select label="Issue type" options={{
            bug: 'Bug',
            feature_request: 'Feature Request',
            feedback: 'Feedback',
            security: 'Security'
          }}
                  onChange={this.updateChange} name="type" />
          <TextArea label="Description" value={this.state.issue.body}
                    onChange={this.updateChange} name="body" />
          <Submit onClick={this.handleClick} />
        </form>
      </div>
    );
  }
}

export default IssueForm