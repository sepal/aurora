import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './style.scss';

function Comment(props) {
  return (
    <div styleName='comment'>
      <div>
        <i className="fa fa-user"></i> {props.author}
      </div>
      <div>
        {props.comment}
      </div>
    </div>
  );
}

export default CSSModules(Comment, styles)
