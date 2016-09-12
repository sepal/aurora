import React from 'react';
import styles from './style.scss';

const Submit = function (props) {
  return (
    <div className={styles.submit}>
      <button type="submit" onClick={props.onClick}>{props.value}</button>
    </div>
  );
};

Submit.propTypes = {
  value: React.PropTypes.string,
  onClick: React.PropTypes.func
};

Submit.defaultProps = {
  value: "Submit",
  onClick: (e) => {
    e.preventDefault();
  }
};

export default Submit;