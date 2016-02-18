from json import loads
from hashlib import sha1
import hmac

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.conf import settings

from users.models import User
from webhooks.models import Webhooks


def save_debug_webhook(status, request):
    status = "{} {}".format(status, request.META.get('HTTP_X_HUB_SIGNATURE'))
    if settings.FACEBOOK_WEBHOOK_DEBUG:
        Webhooks.objects.create(status=status, data=request.body)


def get_error(request, message):
    save_debug_webhook("FAIL {}".format(message), request)
    return HttpResponseBadRequest(message)


def get_response(request, message):
    save_debug_webhook("OK {}".format(message), request)
    return HttpResponse(message)


class WebhooksView(View):

    def _verify_post_signature(self, request):
        x_hub_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
        if x_hub_signature is None:
            return False

        sha_name, signature = x_hub_signature.split('=')
        if sha_name != 'sha1':
            return False

        body = request.body
        key = settings.SOCIAL_AUTH_FACEBOOK_SECRET
        my_sign = hmac.new(key, body, sha1)
        return my_sign.hexdigest() == signature

    def post(self, request, *args, **kwargs):
        body = request.body

        data = loads(body)
        if 'object' not in data or data['object'] != 'user' or \
                'entry' not in data:
            return get_error(request, 'Invalid webhook')

        if not self._verify_post_signature(request):
            return get_error(request, 'Invalid signature')

        for entry in data['entry']:
            if 'id' not in entry:
                return get_error(request, 'Invalid webhook')

            uid = entry['id']

            if not User.objects.filter(uid=uid).exists():
                return get_error(request, 'Invalid user id')

            user = User.objects.get(uid=uid)

            user.update_friends()

        return get_response(request, 'Ok')

    def get(self, request, *args, **kwargs):
        mode = request.GET.get('hub.mode')
        challenge = request.GET.get('hub.challenge')
        verify_token = request.GET.get('hub.verify_token')

        if mode is None or challenge is None or verify_token is None:
            return HttpResponseBadRequest('Bad request')

        if verify_token != settings.FACEBOOK_WEBHOOK_TOKEN:
            return HttpResponseBadRequest('Invalid token')

        return HttpResponse(challenge)


class WebhooksDebugView(View):

    def get(self, request, *args, **kwargs):
        webhooks = Webhooks.objects.all()
        body = ["{} - {}".format(w.status, w.data) for w in webhooks]
        return HttpResponse("<br />".join(body))
