import React from 'react'
import ChatInput from "./input"
import MessageList from "./message_list"

class Chat extends React.Component {
  constructor(props) {
    super(props)

    this.state = {messages: [], questions: []}
  }

  addMessage = (message) => {
    let messages = [...this.state.messages, {text: message["message"], username: message["username"]}]
    this.setState({messages})
  }

  render() {
    return (
      <div>
        <MessageList messages={this.state.messages}/>
        <ChatInput onInput={this.onInput}/>
      </div>
    )
  }

  join = (room) => {
    if (!room) return;

    if (this.socket && this.socket.readyState === WebSocket.OPEN) this.socket.close();
    console.log("connecting to " + window.location.host);
    this.socket = new WebSocket("ws://" + window.location.hostname + ":8000/" + room);

    document.getElementById("chat").innerHTML = '';

    this.socket.onmessage = (e) => {
      let data = JSON.parse(e.data);
      const {messages} = this.state
      this.setState({messages: [...messages, {text: data["message"], username: data["username"]}]})
    };

    this.socket.onopen = () => {
      let msg = document.createElement("p");
      let text = document.createTextNode("Current room: " + room);
      msg.appendChild(text);
      let roomDisplay = document.getElementById("room");
      if (roomDisplay.firstChild) {
        roomDisplay.replaceChild(msg, roomDisplay.firstChild);
      } else {
        roomDisplay.appendChild(msg);
      }
    };
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
