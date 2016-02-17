import FriendsListItem from '../../scripts/components/friends-list-item'

import User from '../../scripts/stores/definitions/user'

const user = new User({
  firstName: 'Leo',
  lastName: 'Nnc',
  uid: 2349231234
})

describe('FriendsListItem', () => {
  it('render', () => {
    const elem = $R(TestUtils.renderIntoDocument(
      <FriendsListItem friend={user} />
    ))

    expect(elem.find('.FriendsListItem-name').text()).to.be.equal(user.fullName)
    expect(elem.find('.FriendsListItem-picture').get(0)).to.have.prop('src', user.picture)
  })
})
