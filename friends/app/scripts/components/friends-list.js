import React from 'react'
import Promise from 'bluebird'

import userStore from '../stores/user-store'

import FriendsListItem from './friends-list-item'

export default React.createClass({
  displayName: 'FriendsList',

  getInitialState() {
    return {
      user: null,
      friends: null,
      error: null,
      canRender: false
    }
  },

  componentWillMount() {
    Promise.join(
      userStore.getMyInfo(),
      userStore.getFriends(),
    (user, friends) => {
      if (this.isMounted()) {
        this.setState({
          user,
          friends,
          canRender: true
        })
      }
    })
    .catch(({message}) => {
      this.isMounted() && this.setState({error: message})
    })
  },

  _getWelcomeMessage() {
    const {user, friends} = this.state

    let message
    if (friends.isEmpty()) {
      message = 'It looks like none of your friends is using this App!'
    } else {
      message = `This is the list of your friends (${friends.size}) using this App.`
    }
    return (
      <div className='FriendsList-welcome'>
        <h1>Welcome <span className='FriendsList-welcome-user'>{user.fullName}</span>!</h1>
        <h2 className='FriendsList-welcome-message'>{message}</h2>
      </div>
    )
  },

  render() {
    if (this.state.error) {
      return <div className='errorBlock'>{this.state.error}</div>
    } else if (!this.state.canRender) {
      return null
    }

    const {friends} = this.state

    const children = friends.map((f, i) => <FriendsListItem friend={f} key={i} />)

    return (
      <div className='FriendsList'>
        {this._getWelcomeMessage()}
        <div className='FriendsList-list'>
          {children}
        </div>
      </div>
    )
  }
})
