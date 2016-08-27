import React from 'react';
import {Link} from 'react-router';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import IssueLabel from '../IssueLabel';

function IssueTeaser(props) {
  let upvote_label = props.upvotes == 1 ? "upvote" : "upvotes";
  let comment_label = props.comments == 1 ? "comment" : "comments";
  return (
    <Link
      key={props.id}
      to={{
        pathname: `/gsi/feedback/issue/${props.id}`,
        state: { returnTo: '/gsi/feedback' }
      }}
      styleName="issueTeaser"
    >
      <IssueLabel type={props.type} title={props.title}/>
      <div styleName="footer">
        <span styleName="upvotes">
          <i className="fa fa-thumbs-up"></i> {props.upvotes} {upvote_label}
        </span>
        <span styleName="comments">
          <i className="fa fa-comments"></i> {props.comments} {comment_label}
        </span>
      </div>
    </Link>
  );
}

export default CSSModules(IssueTeaser, styles)
