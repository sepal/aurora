import React from 'react'
import ChatInput from "./input"
import MessageList from "./message_list"

import './chat.css'

class Chat extends React.Component {
  constructor(props) {
    super(props)

    this.state = {messages: [], questions: []}
  }

  componentDidMount = () => {
    this.join('main')
    this.scrollToBottom()
  }

  render = () => {
    return (
      <div ref="_chat" className="Chat">
        <MessageList messages={this.state.messages}/>
        <ChatInput onInput={this.onInput}/>
        <div ref="_end"></div>
      </div>
    )
  }

  handleMessage = (message) => {
    if (message['type'] === 'chat-message') {
      message['logged_in_user'] = this.state['username']
      const {messages} = this.state
      this.setState({messages: [...messages, message]})
    } else if (message['type'] === 'whoami') {
      this.setState({username: message['username']})
    }

    this.scrollToBottom()
  }

  scrollToBottom = () => {
    this.refs._end.scrollIntoView({behavior: 'smooth'})
  }

  join = (room) => {
    if (!room) return;

    if (this.socket && this.socket.readyState === WebSocket.OPEN) this.socket.close();

    let proto
    proto = window.location.protocol === 'https:' ? 'wss://' : 'ws://'

    let port
    switch (window.location.port) {
      case '3000':
        // This is a special case for dev where the site is served by `yarn start` and ws should connect to
        // the django backend on port `8000`
        port = ':8000'
        break;
      case '':
        port = ''
        break;
      default:
        port = ':' + window.location.port
        break;
    }

    let uri = proto + window.location.hostname + port + "/ws/" + room
    this.socket = new WebSocket(uri);

    this.setState({messages: []})

    this.socket.onmessage = (e) => {
      let data = JSON.parse(e.data);
      this.handleMessage(data)
    }

    this.socket.onopen = () => {
    }
  }

  onInput = (value) => {
    if (value.startsWith('/join ')) {
      const room = value.split(' ')[1]
      this.join(room)
      return
    }

    let message

    if (value.startsWith('/ask ')) {
      message = {
        "type": "question",
        "text": value.replace(/^\/ask /, '')
      }
    } else {
      message = {
        "type": "chat-message",
        "text": value
      }
    }

    if (this.socket.readyState === WebSocket.OPEN) this.socket.send(JSON.stringify(message));
  }
}

export default Chat
