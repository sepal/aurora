import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

function IssueList(props) {
  const issues = props.issues.map(issue => {
    return (
      <li key={issue.id} styleName="issue">
        <div>
          <div>{issue.title}</div>
          <div styleName="footer">
            <span styleName="upvotes"><i className="fa fa-thumbs-up"></i> {issue.upvotes} upvotes</span>
            <span styleName="comments"><i className="fa fa-comments"></i> {issue.comments} comments</span>
          </div>
        </div>
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
