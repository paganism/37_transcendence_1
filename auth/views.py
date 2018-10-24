from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


def index(request):
    """
    function for index page
    """
    return render(
        request,
        'index.html',
        context={
        },
    )


def user_profile(request, pk):
    """
    function for user page
    """
    # user = get_object_or_404(User, pk=pk)
    user = 2
    return render(
        request,
        'user_profile.html',
        context={
            'user': user
        },
    )
