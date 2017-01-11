import React from 'react';

import styles from './style.scss';
import IssueTeaser from '../IssueTeaser';

export default function IssueList(props) {
  const issues = props.issues.map(issue => {
    let number_comments = 0;
    let upvotes = 0;

    if (issue['comments'] !== undefined) {
      return number_comments = issue.comments.length;
    }

    if (issue['upvotes'] !== undefined) {
      return upvotes = issue['upvotes'];
    }

    return (
      <li key={issue.id} className={styles.item}>
        <IssueTeaser title={issue.title} upvotes={upvotes}
                     comments={number_comments} id={issue.id} type={issue.type}
                     lane={issue.lane.id} />
      </li>
    );
  });
  const msg = (
    <li className={styles.empty}>
    No issues here yet.
    </li>
  );
  return (
    <ul>
      { issues.length > 0 ? issues : msg }
    </ul>
  );
}
