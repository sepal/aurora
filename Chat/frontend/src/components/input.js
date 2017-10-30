import React from 'react'
import PropTypes from 'prop-types'

const ChatInput = ({onInput}) =>
  <div>
    <input id="msgInput" className="ChatInput"
           onKeyDown={
             (event) => {
               if (event.keyCode === 13) {
                 onInput(event.target.value)
                 event.target.value = ""
               }
             }
           }
    />
  </div>

ChatInput.propTypes = {
  onSend: PropTypes.func
}

ChatInput.defaultProps = {
  onInput: f => f
}

export default ChatInput
