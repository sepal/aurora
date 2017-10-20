import React from 'react'
import {render} from 'react-dom'

import Chat from './components/chat'

render(
  <div>
    <div id="room"></div>
    <div id="chat"></div>
    <Chat />
  </div>,

  document.getElementById('root')
)
