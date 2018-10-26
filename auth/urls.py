from django.urls import include, path

from .views import IndexView, UserProfileView

urlpatterns = [
        path('', IndexView.as_view(), name='index'),
    ]
urlpatterns += [
        path('user/<pk>/', UserProfileView.as_view(), name='user_profile'),
]
