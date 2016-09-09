import React from 'react';
import styles from './style.scss';

export default function IssueLabel(props) {
  var label = '';
  switch (props.type) {
    case 'bug':
      label = 'Bug';
      break;
    case 'feature_request':
      label = 'Feature Request';
      break;
    case 'feedback':
      label = 'Feedback';
      break;
    case 'security':
      label = 'Security';
      break;
  }

  return (
    <div>
      <span className={styles.issueTypeLabel}>[{label}]</span> {props.title}
    </div>
  );
}
