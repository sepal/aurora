import React from 'react';
import styles from './style.scss';

import { unique_id } from '../../../utilities';

const TextInput = (props) => {
  let id = unique_id(props.label);
  return (
    <div className={styles.text_input}>
      <label htmlFor={id}>{props.label}:</label>
      <input id={id} value={props.value} size={props.size}/>
    </div>
  );
};

TextInput.propTypes = {
  label: React.PropTypes.string,
  value: React.PropTypes.string,
  size: React.PropTypes.number
};

TextInput.defaultProps = {
  size: 64
};

export default TextInput;