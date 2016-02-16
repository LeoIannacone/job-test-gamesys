import I from 'immutable'

export default class User extends I.Record({
  uid: 0,
  firstName: '',
  lastName: ''
}) {
  get fullName() {
    return `${this.firstName} ${this.lastName}`
  }

  get picture() {
    return `https://graph.facebook.com/${this.uid}/picture?type=large`
  }
}
