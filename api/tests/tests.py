from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from users.tests.factories import UsersFactory

from api.views import ApiFriendsView, ApiMeView


class ApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()

    def test_me_ok(self):
        user = UsersFactory.create()
        url = reverse('api:me', )
        request = self.factory.get(url)
        request.user = user
        response = ApiMeView.as_view()(request)
        self.assertEqual(response.data['code'], 1)
        data_r = response.data['response']

        self.assertEqual(data_r['first_name'], user.first_name)
        self.assertEqual(data_r['last_name'], user.last_name)
        self.assertEqual(data_r['uid'], user.uid)

    def test_me_fails_if_user_is_not_logged(self):
        url = reverse('api:me', )
        response = self.client.get(url)
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['message'], 'User not logged')

    def test_friends_ok(self):
        user = UsersFactory.create()
        f1 = UsersFactory.create()
        f2 = UsersFactory.create()
        user.friends.add(f1)
        user.friends.add(f2)
        url = reverse('api:friends', )
        request = self.factory.get(url)
        request.user = user
        response = ApiFriendsView.as_view()(request)
        self.assertEqual(response.data['code'], 1)
        data_r = response.data['response']

        self.assertEqual(len(data_r), 2, "User has 2 friends")

        check_1 = f1
        check_2 = f2
        if data_r[0]['uid'] == f2.uid:
            check_2 = f1
            check_1 = f2

        self.assertEqual(data_r[0]['first_name'], check_1.first_name)
        self.assertEqual(data_r[0]['last_name'], check_1.last_name)
        self.assertEqual(data_r[0]['uid'], check_1.uid)

        self.assertEqual(data_r[1]['first_name'], check_2.first_name)
        self.assertEqual(data_r[1]['last_name'], check_2.last_name)
        self.assertEqual(data_r[1]['uid'], check_2.uid)

    def test_friends_fails_if_user_is_not_logged(self):
        url = reverse('api:friends', )
        response = self.client.get(url)
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['message'], 'User not logged')
