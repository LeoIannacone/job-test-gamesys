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

  render() {
    if (this.state.error) {
      return <div className='errorBlock'>{this.state.error}</div>
    } else if (!this.state.canRender) {
      return null
    }

    const {user, friends} = this.state

    const children = friends.map((f, i) => <FriendsListItem friend={f} key={i} />)

    return (
      <div className='FriendsList'>
        <div className='FriendsList-user'>
          Welcome <span>{user.fullName}</span>, this is the list of your friends using this App!
        </div>
        <div className='FriendsList-list'>
          {children}
        </div>
      </div>
    )
  }
})
