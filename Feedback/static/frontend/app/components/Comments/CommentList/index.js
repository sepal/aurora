import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

import Comment from "../Comment";


function CommentList(props) {
  const comments = props.comments.map(comment => {
    return (
      <li key="comment.id">
        <Comment author={comment.author}
            pic={comment.pic}
            comment={comment.comment}
            post_date={comment.post_date}/>
      </li>
    );
  });

  return (
    <ul>
      {comments}
    </ul>
  );
}

export default CSSModules(CommentList, styles)
