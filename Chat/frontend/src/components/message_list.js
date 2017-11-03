import React from 'react'
import ChatMessage from './chat_message'
import PropTypes from 'prop-types'

const MessageList = ({messages}) => {
  let display_author = true;
  const messageList = messages.map((message, i, messages) => {
    if(i > 0) display_author = message.user.name !== messages[i - 1].user.name

    return <ChatMessage key={i} message={message} display_author={display_author}/>
  })

  return (<div className="MessageList">{messageList}</div>)
}

MessageList.propTypes = {
  messages: PropTypes.array
}

MessageList.defaultProps = {
  messages: []
}

export default MessageList
