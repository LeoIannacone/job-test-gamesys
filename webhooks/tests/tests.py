import hmac
from hashlib import sha1
from mock import Mock
from json import dumps
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from django.conf import settings

from users.tests import factories


# Mock update users method
origin_update_friends = factories.models.User.update_friends


class WebhooksPOST_TestCase(TestCase):

    def setUp(self):
        self.client = Client()
        factories.models.User.update_friends = Mock()

    def tearDown(self):
        factories.models.User.update_friends = origin_update_friends

    def _get_body(self, obj='user', entry={'id': -1}):
        return dumps({
            'object': obj,
            'entry': [entry]
        })

    def _get_signature(self, body):
        key = settings.SOCIAL_AUTH_FACEBOOK_SECRET
        return "sha1={}".format(hmac.new(key, body, sha1).hexdigest())

    def test_update_ok(self):
        user = factories.UsersFactory.create()
        body = self._get_body(entry={'id': user.uid})

        signature = self._get_signature(body)

        url = reverse('webhooks', )
        response = self.client.post(url, body,
                                    content_type="application/json",
                                    **{'HTTP_X_HUB_SIGNATURE': signature})
        self.assertEqual(response.content, 'Ok')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.update_friends.called)

    def test_update_fails_with_wrong_body(self):
        body = self._get_body(obj='wrong object')
        url = reverse('webhooks', )
        response = self.client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Invalid webhook')

    def test_update_fails_with_wrong_uid(self):
        body = self._get_body()
        url = reverse('webhooks', )
        signature = self._get_signature(body)
        response = self.client.post(url, body,
                                    content_type="application/json",
                                    **{'HTTP_X_HUB_SIGNATURE': signature})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Invalid user id')

    def test_update_fails_with_wrong_signature(self):
        user = factories.UsersFactory.create()
        body = self._get_body(entry={'id': user.uid})
        url = reverse('webhooks', )
        response = self.client.post(url, body,
                                    content_type="application/json",
                                    **{'HTTP_X_HUB_SIGNATURE': 'sha1=invalid'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Invalid signature')
        self.assertFalse(user.update_friends.called)


class WebhooksGET_TestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def _get_query(self, challenge='test challenge',
                   mode='subscribe',
                   token=settings.FACEBOOK_WEBHOOK_TOKEN):
        return {
            'hub.mode': mode,
            'hub.verify_token': token,
            'hub.challenge': challenge
        }

    def test_verification_ok(self):
        url = reverse('webhooks', )
        challenge = 'get OK test challenge'
        response = self.client.get(url, self._get_query(challenge=challenge))
        self.assertEqual(response.status_code, 200)
        # must return the challange
        self.assertEqual(response.content, challenge)

    def test_verification_fail_with_invalid_params(self):
        url = reverse('webhooks', )
        response = self.client.get(url, )
        self.assertEqual(response.status_code, 400)

    def test_verification_fail_with_wrong_token(self):
        url = reverse('webhooks', )
        response = self.client.get(url, self._get_query(token='false token'))
        # must fail with invalid token
        self.assertEqual(response.status_code, 400)
