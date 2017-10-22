import React from 'react'

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

ChatMessage.defaultProps = {
  message: {text: '', user: {name: '', is_staff: false}}
}

export default ChatMessage
