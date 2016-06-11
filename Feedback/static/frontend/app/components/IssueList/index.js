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
            <span styleName="upvotes"><li className="fa fa-thumbs-up"></li> {issue.upvotes} upvotes</span>
            <span styleName="comments"><li className="fa fa-comments"></li> {issue.comments} comments</span>
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
