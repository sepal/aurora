import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import IssueMockup from '../../mockup/issues';

class IssueDetail extends React.Component {
  constructor(props) {
    super(props);
    const issues = IssueMockup.filter(issue => {
      return issue.id == props.params.id
    });

    if (issues.length != 0) {
      this.state = {
        issue: issues[0]
      }
    }

  }
  render() {
    return (
      <div styleName='issueDetail'>
        <div styleName="title">{this.state.issue.title}</div>
        <div styleName="body">{this.state.issue.body}</div>
      </div>
    );
  }
}

export default CSSModules(IssueDetail, styles)
