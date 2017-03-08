import Moment from 'moment';
import React, {PropTypes, Component} from 'react';

import styles from './style.scss';
import IssueLabel from '../IssueLabel'
import IssueIcon from '../IssueIcon';
import IssueBody from '../IssueBody';

import Comments from '../../Comments';

export default class IssueDetail extends Component {
  static propTypes = {
    id: PropTypes.number.isRequired,
    type: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    isAuthor: PropTypes.bool,
    canDrag: PropTypes.bool,
    upvotes: PropTypes.number,
    comments: PropTypes.number,
    preview: PropTypes.bool,
    body: PropTypes.string
  };

  constructor(props) {
    super(props);

    this.onLabelTypeChange = this.onLabelTypeChange.bind(this);
    this.onBodyChange = this.onBodyChange.bind(this);
    this.onUpvote = this.onUpvote.bind(this);
  }

  render() {
    const upvote_label = this.props.upvotes == 1 ? "upvote" : "upvotes";
    const date = Moment(this.props.post_date).calendar();
    const canEdit = this.props.isAuthor || this.props.isStaff;

    let upvote_action = <button onClick={this.onUpvote}><i className="fa fa-thumbs-up"></i> upvote</button>;
    if (this.props.upvoted) {
      upvote_action = <span><i className="fa fa-thumbs-up"></i> upvoted</span>;
    }

    return (
      <div className={styles.issueDetail}>
        <div>
          <div className={styles.title}>
            <span className={styles.icon}>
              <IssueIcon type={this.props.type} />
            </span>
            <IssueLabel
              type={this.props.type}
              title={this.props.title}
              onChange={this.onLabelTypeChange}
              editable={canEdit} />
          </div>
          <div className={styles.subtitle}>
            <span>by {this.props.author.name}</span>&nbsp;
            <span>on {date}</span>,&nbsp;
            <span>{this.props.upvotes ? this.props.upvotes : 0} {upvote_label}</span>
          </div>
        </div>
        <div className={styles.content}>
          <IssueBody className={styles.body} body={this.props.body}
                     onChange={this.onBodyChange} editable={canEdit} />
          <ul className={styles.actions}>
            <li>
              {upvote_action}
            </li>
          </ul>
        </div>
        <Comments issueID={this.props.id} />
      </div>
    );
  }

  renderComments() {
    if (this.props.comments !== undefined && this.props.comments.length > 1) {
      return <CommentList comments={this.props.comments} />
    }
  }

  renderImages() {
    if (this.props.images) {
      const images = this.props.images.map(image => {
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
    this.props.update(this.props.id, type, title, this.props.body);
  }

  onBodyChange(body) {
    this.props.update(this.props.id, this.props.type, this.props.title, body);
  }

  onUpvote() {
    this.props.upvote(this.props.id);
  }
}
