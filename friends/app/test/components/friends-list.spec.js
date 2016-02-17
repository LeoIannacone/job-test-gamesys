import I from 'immutable'
import Promise from 'bluebird'
import faker from 'Faker'
import proxyquire from 'proxyquire'

import User from '../../scripts/stores/definitions/user'

const me = new User({firstName: 'Leo', lastName: 'Nnc'})

const f1 = new User({
  firstName: faker.Name.firstName(),
  lastName: faker.Name.lastName(),
  uid: faker.random.number()
})

const f2 = new User({
  firstName: faker.Name.firstName(),
  lastName: faker.Name.lastName(),
  uid: faker.random.number()
})

const userStore = {}
const resetStores = () => {
  userStore.getMyInfo = sinon.stub().returns(Promise.resolve(me))
  userStore.getFriends = sinon.stub().returns(Promise.resolve(I.List([f1, f2])))
}

const FriendsList = proxyquire('../../scripts/components/friends-list', {
  '../stores/user-store': userStore
})

describe('FriendsList', () => {
  beforeEach(() => {
    resetStores()
  })

  it('renders', () => {
    const elem = $R(TestUtils.renderIntoDocument(
      <FriendsList />
    ))

    return defer(() => {
      expect(elem.find('FriendsListItem')).to.have.length(2)
      expect(elem.find('.FriendsList-welcome-user').text()).to.be.equal(me.fullName)
      expect(elem.find('.FriendsList-welcome-message').text())
        .to.include('list of your friends (2)')
    })
  })

  it('renders a empty lists', () => {
    userStore.getFriends.returns(Promise.resolve(I.List()))
    const elem = $R(TestUtils.renderIntoDocument(
      <FriendsList />
    ))

    return defer(() => {
      expect(elem.find('FriendsListItem')).to.have.length(0)
      expect(elem.find('.FriendsList-welcome-user').text()).to.be.equal(me.fullName)
      expect(elem.find('.FriendsList-welcome-message').text()).to.include('none of your friends')
    })
  })

  it('handle errors', () => {
    const error = 'Test error'
    userStore.getFriends.returns(Promise.reject(new Error(error)))
    const elem = $R(TestUtils.renderIntoDocument(
      <FriendsList />
    ))

    return defer(() => {
      expect(elem.find('FriendsListItem')).to.have.length(0)
      expect(elem.find('.errorBlock').text()).to.include(error)
    })
  })
})
