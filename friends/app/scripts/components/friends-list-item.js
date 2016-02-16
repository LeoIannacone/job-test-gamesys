import React from 'react'

import User from '../stores/definitions/user'

export default React.createClass({
  displayName: 'FriendsListItem',

  propTypes: {
    friend: React.PropTypes.instanceOf(User).isRequired
  },

  render() {
    const {friend} = this.props

    return (
      <div className='FriendsListItem'>
        <img className='FriendsListItem-picture' src={friend.picture} />
        <div className='FriendsListItem-name'>{friend.fullName}</div>
      </div>
    )
  }
})
