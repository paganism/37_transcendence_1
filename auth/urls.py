from django.urls import include, path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('index/', views.index, name='index'),
    ]
urlpatterns += [
        path('user/<pk>/', views.user_profile, name='user_profile'),
]
