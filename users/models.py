import json
import requests
import facebook

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uid = models.CharField(max_length=120, primary_key=True)
    friends = models.ManyToManyField('self')

    def update_friends(self):
        app_key = settings.SOCIAL_AUTH_FACEBOOK_APP_KEY
        app_secret = settings.SOCIAL_AUTH_FACEBOOK_APP_SECRET
        token = facebook.get_app_access_token(app_key, app_secret)
        graph = facebook.GraphAPI(token)
        info = graph.get_connections(self.uid, 'friends')

        while True:
            self._update_raw_friends(info.get('data'))
            has_next = 'paging' in info and 'next' in info['paging']
            if not has_next:
                break
            next_url = info['paging']['next']
            info = json.loads(requests.get(next_url).text)

    def _update_raw_friends(self, data):
        for raw_friend in data:
            uid = raw_friend.get('id')
            if self.friends.filter(uid=uid).exists():
                continue
            info_name = raw_friend.get('name')
            if ' ' in info_name:
                info_name = info_name.split(' ')
                (first_name, last_name) = (info_name[0], info_name[1])
            else:
                (first_name, last_name) = (info_name, '')
            (friend, created) = User.objects.get_or_create(uid=uid, defaults={
                'first_name': first_name,
                'last_name': last_name,
                'username': uid,
                'uid': uid
            })
            friend.friends.add(self)
            self.friends.add(friend)
