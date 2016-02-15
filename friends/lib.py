import json
import requests
import facebook
from django.conf import settings

from users.models import User


def _frow_raw_to_friend(user, data):
    for raw_friend in data:
        uid = raw_friend.get('id')
        if user.friends.filter(uid=uid).exists():
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
        friend.friends.add(user)
        user.friends.add(friend)


def update_friends(user):
    app_key = settings.SOCIAL_AUTH_FACEBOOK_APP_KEY
    app_secret = settings.SOCIAL_AUTH_FACEBOOK_APP_SECRET
    token = facebook.get_app_access_token(app_key, app_secret)
    graph = facebook.GraphAPI(token)
    info = graph.get_connections(user.uid, 'friends')

    while True:
        _frow_raw_to_friend(user, info.get('data'))
        has_next = 'paging' in info and 'next' in info['paging']
        if not has_next:
            break
        next_url = info['paging']['next']
        info = json.loads(requests.get(next_url).text)
