import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import IssueTeaser from '../IssueTeaser';

function IssueList(props) {
  const issues = props.issues.map(issue => {
    return (
      <li key={issue.id} styleName="item">
        <IssueTeaser title={issue.title} upvotes={issue.upvotes}
                     comments={issue.comments} id={issue.id} type={issue.type} />
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
