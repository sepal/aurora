import React from 'react'
import PropTypes from 'prop-types'

const Question = ({text, username}) => {
  return (
    <div class="question">
      <div class="headline">
        <p class="username">{username}</p>
      </div>
      <p class="text">{text}</p>
    </div>
  )
}

Question.propTypes = {
  text: PropTypes.string,
  username: PropTypes.string,
}

Question.defaultProps = {
  text: "",
  username: ""
}

export default Question
