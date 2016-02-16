import User from '../definitions/user'

export default {
  getUserFromData(data) {
    return new User({
      uid: data.get('uid'),
      lastName: data.get('last_name'),
      firstName: data.get('first_name')
    })
  }
}
