from django.urls import include, path

from .views import IndexView, UserProfileView, register, login_view

# urlpatterns = [
#         path('', IndexView.as_view(), name='index'),
#     ]

urlpatterns = [
    path('accounts/login/', login_view, name='index'),
]

urlpatterns += [
        path('user/<pk>/', UserProfileView.as_view(), name='user_profile'),
]

urlpatterns += [
    path('register/', register, name='register'),
]