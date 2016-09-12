import React from 'react';
import styles from './style.scss';

import {unique_id} from '../../../utilities';

const Select = (props) => {
  const id = unique_id(props.label);

  let options = [];
  for (let key in props.options) {
    options.push(<option value={key}>{props.options[key]}</option>);
  }

  return (
    <div className={styles.select}>
      <label htmlFor={id}>{props.label}:</label>
      <select>
        {options}
      </select>
    </div>
  );
};

export default Select;