from json import loads
from hashlib import sha1

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from users.models import User
from webhooks.models import Webhooks


def save_debug_webhook(status, data):
    if settings.FACEBOOK_WEBHOOK_DEBUG:
        Webhooks.objects.create(status=status, data=data)


def get_error(request, message):
    save_debug_webhook("FAIL {}".format(message), request.body)
    return HttpResponseBadRequest(message)


def get_response(request, message):
    save_debug_webhook("OK {}".format(message), request.body)
    return HttpResponse(message)


class WebhooksView(View):

    def _verify_post_signature(self, request):
        if 'X-Hub-Signature' not in request.META:
            return False
        signature = request.META.get('X-Hub-Signature')[5:]  # remove the sha1=
        body = request.body
        key = settings.FACEBOOK_WEBHOOK_TOKEN
        my_sign = sha1("{}{}".format(key, body)).hexdigest()
        return my_sign == signature

    def post(self, request, *args, **kwargs):
        body = request.body

        data = loads(body)
        if 'object' not in data or data['object'] != 'user' or \
                'entry' not in data or 'id' not in data['entry']:
            return get_error(request, 'Invalid webhook')

        uid = data['entry']['id']

        if not User.objects.filter(uid=uid).exists():
            return get_error(request, 'Invalid user id')

        user = User.objects.get(uid=uid)

        if not self._verify_post_signature(request):
            return get_error(request, 'Invalid signature')

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


class WebhooksDebugView(APIView):

    def _webhook_to_dict(self, w):
        return {
            'status': w.status,
            'body': loads(w.data)
        }

    def get(self, request, *args, **kwargs):
        webhooks = Webhooks.objects.all()
        body = [self._webhook_to_dict(w) for w in webhooks]
        return Response(body)
