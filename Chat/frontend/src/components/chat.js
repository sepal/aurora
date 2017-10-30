import React from 'react'
import ChatInput from "./input"
import MessageList from "./message_list"

import './chat.css'

class Chat extends React.Component {
  constructor(props) {
    super(props)

    this.state = {messages: [], questions: []}
  }

  componentDidMount() {
    this.join('main')
  }

  addMessage = (message) => {
    let messages = [...this.state.messages, {text: message["message"], username: message["username"]}]
    this.setState({messages})
  }

  render() {
    return (
      <div className="Chat">
        <MessageList messages={this.state.messages}/>
        <ChatInput onInput={this.onInput}/>
      </div>
    )
  }

  join = (room) => {
    if (!room) return;

    if (this.socket && this.socket.readyState === WebSocket.OPEN) this.socket.close();
    console.log("connecting to " + window.location.host);
    this.socket = new WebSocket("ws://" + window.location.hostname + ":8000/ws/" + room);

    this.setState({messages: []})

    this.socket.onmessage = (e) => {
      let data = JSON.parse(e.data);
      const {messages} = this.state
      this.setState({messages: [...messages, data]})
    }

    this.socket.onopen = () => {
      console.log('joined room ' + room)
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
