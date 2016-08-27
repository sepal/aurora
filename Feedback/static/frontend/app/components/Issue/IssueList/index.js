import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import IssueTeaser from '../IssueTeaser';

function IssueList(props) {
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
      <li key={issue.id} styleName="item">
        <IssueTeaser title={issue.title} upvotes={upvotes}
                     comments={number_comments} id={issue.id} type={issue.type} />
      </li>
    );
  });
  return (
    <ul>
      {issues}
    </ul>
  );
}

export default CSSModules(IssueList, styles)
