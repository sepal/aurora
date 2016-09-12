import React from 'react';
import styles from './style.scss';

import { unique_id } from '../../../utilities';

const TextArea = (props) => {
  let id = unique_id(props.label);
  return (
    <div className={styles.text_area}>
      <label htmlFor={id}>{props.label}:</label>
      <textarea rows={props.rows}>
        {props.value}
      </textarea>
    </div>
  );
};

TextArea.propTypes = {
  label: React.PropTypes.string,
  value: React.PropTypes.string,
  rows: React.PropTypes.number
};

TextArea.defaultProps = {
  rows: 10,
};

export default TextArea;