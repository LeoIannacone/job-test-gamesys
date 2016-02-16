import helper from '../../helpers/user-helper'
import request from '../request'

export default {
  getMyInfo() {
    return request('me')
    .then(helper.getUserFromData)
  },

  getFriends() {
    return request('friends')
    .then(data => data.map(helper.getUserFromData))
  }
}
