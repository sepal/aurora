import Moment from 'moment';
import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';
import CommentList from '../CommentList';

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

  renderIcon() {
    switch (this.state.type) {
      case 'Feature Request':
        return <i className="fa fa-lightbulb-o"></i>;
      case 'Bug':
        return <i className="fa fa-bug"></i>;
      case 'Feedback':
        return <i className="fa fa-commenting-o"></i>;
    }
  }

  renderComments() {
    if (this.state.comments.length > 1) {
      return (
        <div styleName="comments">
          <h2>Comments:</h2>
          <CommentList comments={this.state.comments} />
        </div>
      );
    }
  }

  render() {
    const upvote_label = this.state.upvotes > 1 ? "upvotes" : "upvote";
    const date = Moment.unix(this.state.post_date).calendar();

    return (
      <div styleName='issueDetail'>
        <div>
          <div styleName="title">
            <span styleName="icon">
            {this.renderIcon()}
            </span>
            <span styleName="type">[{this.state.type}]</span> {this.state.title}
          </div>
          <div styleName="subtitle">
            <span>by {this.state.author}</span>&nbsp;
            <span>on {date}</span>,&nbsp;
            <span>{this.state.upvotes} {upvote_label}</span>
          </div>
        </div>
        <div styleName="content">
          <div styleName="body">{this.state.body}</div>
          <ul styleName="actions">
            <li>
              <button><i className="fa fa-thumbs-up"></i> upvote</button>
            </li>
            <li>
              <button><i className="fa fa-eye"></i> subscribe</button>
            </li>
          </ul>
        </div>
        {this.renderComments()}
      </div>
    );
  }
}

export default CSSModules(IssueDetail, styles)
