from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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
