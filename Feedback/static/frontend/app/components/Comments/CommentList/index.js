import React from 'react';
import styles from './style.scss';

import Comment from "../Comment";


export default function CommentList(props) {
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
