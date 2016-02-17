from rest_framework.views import APIView
from rest_framework.response import Response


def response_error(message):
    return Response({'code': 0, 'message': message})


def response(body):
    return Response({'code': 1, 'response': body})


class RestrictedView(APIView):

    def _from_user_to_obj(self, user):
        return {
            'uid': user.uid,
            'first_name': user.first_name,
            'last_name': user.last_name
        }

    def get(self, request, format=None):
        user = request.user
        if user.is_anonymous():
            return response_error('User not logged')
        return self.get_response(user)

    def get_response(self, user):
        pass


class ApiFriendsView(RestrictedView):

    def get_response(self, user):
        body = []
        for f in user.friends.all():
            body.append(self._from_user_to_obj(f))
        return response(body)


class ApiMeView(RestrictedView):

    def get_response(self, user):
        return response(self._from_user_to_obj(user))
