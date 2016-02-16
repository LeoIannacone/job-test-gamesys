import React from 'react'
import ReactDOM from 'react-dom'

import FriendsList from './components/friends-list'

const Main = React.createClass({
  displayName: 'Main',

  render() {
    return <FriendsList />
  }
})

ReactDOM.render(<Main />, document.getElementById('main'))
