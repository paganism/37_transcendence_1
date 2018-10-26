from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class IndexView(generic.TemplateView):
    template_name = "index.html"


class UserProfileView(LoginRequiredMixin, generic.DetailView):

    model = User

    # @login_required
    def book_detail_view(self, request, pk):
        try:
            user_id = User.objects.get(pk=pk)
        except User.DoesNotExists:
            raise Http404("User does not exists")
        return render(
            request,
            'templates/user_detail.html',
            context={'user': user_id}
        )
