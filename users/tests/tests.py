from django.test import TestCase

import factories


class Stub(object):

    def __init__(self, *args):
        pass


def dummy_facebook_get_app_access_token(*args):
    return "test token"


class dummy_request_get(Stub):
    text = """{
        "data": [
            {"id": "30825017510059", "name": "Mario Bros"},
            {"id": "12193683812", "name": "Luigi Maria"}
        ]
    }"""


class dummy_facebbok_GraphAPI(Stub):

    def get_connections(self, *args):
        return {
            'data': [
                {'id': '1660825017510059', 'name': 'Claudia Fiore'},
                {'id': '100412193683812', 'name': 'John Tere'}
            ],
            'paging': {
                'next': 'https://to_next_page'
            },
            'summary': {'total_count': 355}
        }


factories.models.facebook.get_app_access_token = \
    dummy_facebook_get_app_access_token

factories.models.facebook.GraphAPI = \
    dummy_facebbok_GraphAPI

factories.models.requests.get = \
    dummy_request_get


class UsersTestCase(TestCase):

    def test_update_friends(self):
        u = factories.UsersFactory.create()
        u.update_friends()
        self.assertEqual(len(u.friends.all()), 4,
                         "User has 4 friends")
