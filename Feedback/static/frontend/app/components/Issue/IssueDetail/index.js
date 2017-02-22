import Moment from 'moment';
import React from 'react';
import {observer} from 'mobx-react';

import IssueModel from '../../../models/issue';

import styles from './style.scss';
import IssueLabel from '../IssueLabel'
import IssueIcon from '../IssueIcon';

import {CommentList} from '../../Comments';

export default class IssueDetail extends React.Component {
  constructor(props) {
    super(props);

    this.onLabelTypeChange = this.onLabelTypeChange.bind(this);
  }

  render() {
    const upvote_label = this.props.issue.upvotes > 1 ? "upvotes" : "upvote";
    const date = Moment(this.props.issue.post_date).calendar();
    return (
      <div className={styles.issueDetail}>
        <div>
          <div className={styles.title}>
            <span className={styles.icon}>
              <IssueIcon type={this.props.issue.type} />
            </span>
            <IssueLabel
              type={this.props.issue.type}
              title={this.props.issue.title}
              onChange={this.onLabelTypeChange}
              editing={false}/>
          </div>
          <div className={styles.subtitle}>
            <span>by {this.props.issue.author.name}</span>&nbsp;
            <span>on {date}</span>,&nbsp;
            <span>{this.props.issue.upvotes} {upvote_label}</span>
          </div>
        </div>
        <div className={styles.content}>
          <div className={styles.body}>{this.props.issue.body}</div>
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
      </div>
    );
  }

  renderComments() {
    if (this.props.issue.comments !== undefined && this.props.issue.comments.length > 1) {
      return <CommentList comments={this.props.issue.comments} />
    }
  }

  renderImages() {
    if (this.props.issue.images) {
      const images = this.props.issue.images.map(image => {
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

  onLabelTypeChange(type, title) {
    this.props.update(this.props.issue.id, type, title, this.props.issue.body);
  }
}
