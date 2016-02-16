import Reflux from 'reflux'
import UserManager from './api/managers/user-manager'

export default Reflux.createStore({
  getMyInfo() {
    return UserManager.getMyInfo()
  },

  getFriends() {
    return UserManager.getFriends()
  }
})
