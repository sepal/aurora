import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import IssueTeaser from '../IssueList';
import IssueMockup from '../../mockup/issues';

class Lane extends React.Component {
  constructor(props) {
    super(props);
    const issues = IssueMockup.filter(issue => {
      return issue.lane == this.props.id
    });

    this.state = {
      issues: issues
    }
  }
  renderIssueTeaser() {
    return <IssueTeaser issues={this.state.issues} />
  }
  render() {
    let content;

    if (this.state.issues == 0) {
      content = <div styleName="empty">No issues here yet.</div>
    }
    else {
      content = this.renderIssueTeaser();
    }

    return (
      <div styleName='lane'>
        <h2 styleName="title">{this.props.title}</h2>
        <div styleName="content">
          {content}
        </div>
      </div>
    );
  }
}

export default CSSModules(Lane, styles)
