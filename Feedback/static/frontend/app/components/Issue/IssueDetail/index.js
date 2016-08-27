import Moment from 'moment';
import React from 'react';
import CSSModules from 'react-css-modules';
import {observer} from 'mobx-react';

import IssueModel from '../../../models/issue'

import styles from './style.scss';
import {CommentList} from '../../Comments';

@observer
class IssueDetail extends React.Component {
  constructor(props) {
    super(props);
    const issue = new IssueModel();
    issue.loadFromAJAX(props.params.id);

    this.state = issue;
  }

  renderIcon() {
    switch (this.state.type) {
      case 'feature_request':
        return <i className="fa fa-lightbulb-o"></i>;
      case 'bug':
        return <i className="fa fa-bug"></i>;
      case 'feedback':
        return <i className="fa fa-commenting-o"></i>;
    }
  }

  renderComments() {
    if (this.state.comments !== undefined && this.state.comments.length > 1) {
      return <CommentList comments={this.state.comments} />
    }
  }

  renderImages() {
    if (this.state.images) {
      const images = this.state.images.map(image => {
        return (
          <li>
            <a href={image} target="_blank"><img src={image} /></a>
          </li>
        )
      });

      return (
        <ul styleName="images">
          {images}
        </ul>
      )
    }
  }

  render() {
    const upvote_label = this.state.upvotes > 1 ? "upvotes" : "upvote";
    const date = Moment(this.state.post_date).calendar();

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
        {this.renderImages()}
        <div styleName="comments">
          <h2>Comments:</h2>
          <div styleName="new-comment">
            <div styleName="pic">
              <img src="/static/img/8.png" />
            </div>
            <div styleName="textarea">
              <textarea rows="3" placeholder="Create a new comment"></textarea>
            </div>
            <button>Submit</button>
          </div>
          {this.renderComments()}
        </div>
      </div>
    );
  }
}

export default CSSModules(IssueDetail, styles)
