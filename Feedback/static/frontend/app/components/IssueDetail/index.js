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
      this.state = issues[0]
    }

  }

  render() {
    return (
      <div styleName='issueDetail'>
        <div>
          <div styleName="title">
            <i className="fa fa-exclamation-circle" styleName="icon"></i>
            {this.state.title}
          </div>
          <div styleName="author">by {this.state.author}</div>
        </div>
        <div styleName="body">{this.state.body}</div>
      </div>
    );
  }
}

export default CSSModules(IssueDetail, styles)
