import PropTypes from 'prop-types';
import React from 'react';

const Submit = function (props) {
  return (
    <div className="submit">
      <button type="submit" onClick={props.onClick}>{props.value}</button>
    </div>
  );
};

Submit.propTypes = {
  value: PropTypes.string,
  onClick: PropTypes.func
};

Submit.defaultProps = {
  value: "Submit",
  onClick: (e) => {
    e.preventDefault();
  }
};

export default Submit;