from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
# from django.contrib.auth.views import login
from auth.forms import RegistrationForm, LoginForm
from django.contrib.auth import login


class IndexView(generic.TemplateView):
    form = AuthenticationForm()
    fields = ('username', 'password')
    template_name = "registration/login.html"


def login_view(request):
    print('HERE_0')
    if request.method == 'POST':
        print('HERE_1')
        form = LoginForm(request.POST)
        if form.is_valid():
            print('HERE_3')
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print('HERE_4')
            print(user)
            if user:
                print('HERE_6')
                login(request, user)
                # model = User
                # print(request.username)
                print(request.user.id)
                # print(request.user.id)
                # print(request.user.id)

                return redirect('user_profile', request.user.id)
            # else:
            #     return render(request, 'registration/login.html')
    else:
        print('HERE_5')
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
        else:
            return render(request, 'registration/reg_form.html', {'form': form})
    else:
        form = RegistrationForm()
        
        return render(request, 'registration/reg_form.html', {'form': form})


class UserProfileView(LoginRequiredMixin, generic.DetailView):

    model = User

    # @login_required
    def user_detail_view(self, request, pk):
        try:
            user_id = User.objects.get(pk=pk)
            logger.error('There was some crazy error', exc_info=True, extra={
                'request': request,
            })
        except User.DoesNotExists:


            raise Http404("User does not exists")
        return render(
            request,
            'templates/user_detail.html',
            context={'user': user_id}
        )
