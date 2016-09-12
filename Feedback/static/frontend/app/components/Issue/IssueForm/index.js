import React from 'react';
import styles from './style.scss';
import {observer} from 'mobx-react';

import IssueModel from '../../../models/issue';
import {TextInput, TextArea, Select, Submit} from '../../forms';

@observer
class IssueForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = new IssueModel();
  }

  componentDidMount() {
    if (this.props.params) {
      this.state.loadFromAJAX(this.props.params.id);
    }
  }

  handleClick(event) {
    event.preventDefault();
  }

  render() {
    return (
      <div className={styles.issueForm}>
        <form>
          <TextInput label="Title" value={this.state.title} onChange={this.state.} />
          <Select label="Issue type" options={this.state.options()} />
          <TextArea label="Description" value={this.state.body} />
          <Submit onClick={this.handleClick} />
        </form>
      </div>
    );
  }
}

export default IssueForm