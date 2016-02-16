import React from 'react'

import User from '../stores/definitions/user'

export default React.createClass({
  displayName: 'FriendsListItem',

  propTypes: {
    friend: React.PropTypes.instanceOf(User).isRequired
  },

  _getHeader() {
    const {friend} = this.props
    return (
      <div className='FriendsListItem-header'>
        <div className='FriendsListItem-name'>{friend.fullName}</div>
      </div>
    )
  },

  render() {
    const {friend} = this.props

    return (
      <div className='FriendsListItem'>
        {this._getHeader()}
        <img className='FriendsListItem-picture' src={friend.picture} />
      </div>
    )
  }
})
