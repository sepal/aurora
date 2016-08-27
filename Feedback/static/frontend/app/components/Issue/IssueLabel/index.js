import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

function IssueLabel(props) {
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
      <span styleName='issueTypeLabel'>[{label}]</span> {props.title}
    </div>
  );
}

export default CSSModules(IssueLabel, styles)
