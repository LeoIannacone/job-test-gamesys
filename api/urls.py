from django.conf.urls import url

from api.views import ApiFriendsView, ApiMeView

urlpatterns = [
    url(r'^friends/', ApiFriendsView.as_view(), name='friends'),
    url(r'^me/', ApiMeView.as_view(), name='me'),
]
