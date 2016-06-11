import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

function IssueTeaser(props) {
  return (
    <div styleName="issueTeaser">
      <div>{props.title}</div>
      <div styleName="footer">
        <span styleName="upvotes"><i
          className="fa fa-thumbs-up"></i> {props.upvotes} upvotes</span>
        <span styleName="comments"><i
          className="fa fa-comments"></i> {props.comments} comments</span>
      </div>
    </div>
  );
}

export default CSSModules(IssueTeaser, styles)
