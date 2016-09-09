import React from 'react';
import {Link} from 'react-router';
import styles from './style.scss';

import IssueLabel from '../IssueLabel';

export default function IssueTeaser(props) {
  let upvote_label = props.upvotes == 1 ? "upvote" : "upvotes";
  let comment_label = props.comments == 1 ? "comment" : "comments";
  return (
    <Link
      key={props.id}
      to={{
        pathname: `/gsi/feedback/issue/${props.id}`,
        state: { returnTo: '/gsi/feedback' }
      }}
      className={styles.issueTeaser}
    >
      <IssueLabel type={props.type} title={props.title}/>
      <div className={styles.footer}>
        <span className={styles.upvotes}>
          <i className="fa fa-thumbs-up"></i> {props.upvotes} {upvote_label}
        </span>
        <span className={styles.comments}>
          <i className="fa fa-comments"></i> {props.comments} {comment_label}
        </span>
      </div>
    </Link>
  );
}
