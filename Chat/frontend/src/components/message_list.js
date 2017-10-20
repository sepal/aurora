import React from 'react'
import ChatMessage from './chat_message'
import PropTypes from 'prop-types'

const MessageList = ({messages}) => {
  const messageList = messages.map((message, i) =>
    <ChatMessage key={i} message={message.text} username={message.username}/>)

  return (<div>{messageList}</div>)
}

MessageList.propTypes = {
  messages: PropTypes.array
}

MessageList.defaultProps = {
  messages: []
}

export default MessageList
