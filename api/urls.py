from django.conf.urls import url

from api.views import ApiFriendsView, ApiMeView

urlpatterns = [
    url(r'^friends/', ApiFriendsView.as_view()),
    url(r'^me/', ApiMeView.as_view()),
]
