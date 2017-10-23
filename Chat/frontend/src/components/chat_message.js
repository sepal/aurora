import React from 'react'
import PropTypes from 'prop-types'

import './chat_message.css'

const ChatMessage = ({message: {text, user: {name: username, is_staff}}}) => {
  const staffClass = is_staff ? ' staff' : ''
  return (
    <div>
      <div>
        <p className={'ChatMessageAuthor' + staffClass}>{username}</p>
      </div>
      <div>
        <p className='ChatMessageBody'>{text}</p>
      </div>
    </div>
  )
}

// TODO those PropTypes are not working as they're supposed to
ChatMessage.PropTypes = {
  message: PropTypes.shape({
    text: PropTypes.string.isRequired,
    user: PropTypes.shape({
      name: PropTypes.string.isRequired,
      is_staff: PropTypes.bool,
    })
  })
}

ChatMessage.defaultProps = {
  message: {text: '', user: {name: '', is_staff: false}}
}

export default ChatMessage
