def auto_logout(*args, **kwargs):
    """Do not compare current user with new one"""
    return {'user': None}


def save_friends(strategy, details, user=None, *args, **kwargs):
    if user is not None:
        user.update_friends()
    return {'user': user}


def save_uid(strategy, details, user=None, *args, **kwargs):
    if user:
        response = kwargs.get('response', {})
        uid = response.get('id')
        if uid and user.uid != uid:
            user.username = uid
            user.uid = uid
            strategy.storage.user.changed(user)

    return {'user': user}
