import Moment from 'moment';
import React from 'react';
import styles from './style.scss';

const url_regex = /(https?:\/\/[^\s]+)/g;

export default function Comment(props) {
  let comments = props.comment;
  comments = comments.replace(url_regex, url => {
    return `<a href="${url}">${url}</a>`;
  });

  const date = Moment.unix(props.post_date).calendar();

  return (
    <div className={styles.comment}>
      <div className={styles.header}>
        <img className={styles.pic} src={props.pic} />
        <span>{props.author}</span>&nbsp;
        <span className={styles.date}>on {date}</span>
      </div>
      <div className={styles.body}
           dangerouslySetInnerHTML={{__html: comments}}></div>
    </div>
  );
}
