from django.test import TestCase

from mock import Mock
import factories

from utils.tests import Stub

facebook = factories.models.facebook
requests = factories.models.requests

facebook.get_app_access_token = Mock(return_value="text token")

facebook.GraphAPI.__init__ = Mock(return_value=None)
facebook.GraphAPI.get_connections = Mock(return_value={
    'data': [
        {'id': '1660825017510059', 'name': 'Claudia Fiore'},
        {'id': '100412193683812', 'name': 'John Tere'}
    ],
    'paging': {
        'next': 'https://to_next_page'
    },
    'summary': {'total_count': 355}
})


class dummy_request_get(Stub):
    text = """{
        "data": [
            {"id": "30825017510059", "name": "Mario Bros"},
            {"id": "12193683812", "name": "Luigi Maria"}
        ]
    }"""

requests.get = dummy_request_get


class UsersTestCase(TestCase):

    def test_update_friends(self):
        u = factories.UsersFactory.create()
        u.update_friends()
        number_of_friends = len(u.friends.all())
        self.assertEqual(number_of_friends, 4,
                         "User has {} friends".format(number_of_friends))
