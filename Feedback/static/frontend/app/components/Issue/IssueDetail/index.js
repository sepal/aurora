import Moment from 'moment';
import React from 'react';
import {observer} from 'mobx-react';

import IssueModel from '../../../models/issue'

import styles from './style.scss';
import IssueLabel from '../IssueLabel'
import IssueIcon from '../IssueIcon'

import {CommentList} from '../../Comments';

@observer
export default class IssueDetail extends React.Component {
  constructor(props) {
    super(props);
    const issue = new IssueModel();
    this.state = issue;
  }

  componentDidMount() {
    this.state.loadFromAJAX(this.props.params.id);
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
        <ul className={styles.images}>
          {images}
        </ul>
      )
    }
  }

  render() {
    const upvote_label = this.state.upvotes > 1 ? "upvotes" : "upvote";
    const date = Moment(this.state.post_date).calendar();
    return (
      <div className={styles.issueDetail}>
        <div>
          <div className={styles.title}>
            <span className={styles.icon}>
              <IssueIcon type={this.state.type} />
            </span>
            <IssueLabel type={this.state.type} title={this.state.title} />
          </div>
          <div className={styles.subtitle}>
            <span>by {this.state.author}</span>&nbsp;
            <span>on {date}</span>,&nbsp;
            <span>{this.state.upvotes} {upvote_label}</span>
          </div>
        </div>
        <div className={styles.content}>
          <div className={styles.body}>{this.state.body}</div>
          <ul className={styles.actions}>
            <li>
              <button><i className="fa fa-thumbs-up"></i> upvote</button>
            </li>
            <li>
              <button><i className="fa fa-eye"></i> subscribe</button>
            </li>
          </ul>
        </div>
        {this.renderImages()}
        <div className={styles.comments}>
          <h2>Comments:</h2>
          <div className={styles.new-comment}>
            <div className={styles.pic}>
              <img src="/static/img/8.png" />
            </div>
            <div className={styles.textarea}>
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
