import React from 'react'
import PropTypes from 'prop-types'


const ChatMessage = ({message, username, staff}) => {
  return (
    <div>
      <div>
        <p className={'ChatMessageAuthor staff' + staff === 'true' ? 'staff' : ''}>{username}</p>
      </div>
      <div>
        <p className='ChatMessageBody'>{message}</p>
      </div>
    </div>
  )
}

ChatMessage.propTypes = {
  message: PropTypes.string.isRequired,
}

export default ChatMessage
