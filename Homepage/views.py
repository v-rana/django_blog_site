from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView , ListView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView   
from django.views.generic import UpdateView  
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from notes.models import Notes
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, ProfileForm 
from .models import Profile  



class myUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['username'].help_text = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control mb-3'
    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = myUserCreationForm
    success_url = '/login'
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect('/notes')
        return super().get(request, *args, **kwargs)

class LoginInterfaceView(LoginView):
    template_name = 'login.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect('/notes')
        return super().get(request, *args, **kwargs)


class LogoutInterfaceView(LogoutView):
    template_name = 'logout.html'
    
class HomeView(TemplateView):
    template_name = 'home.html'
    extra_context = {'cur_time': datetime.datetime.now()}

class ProfileView(LoginRequiredMixin,ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'profile.html'
    login_url = '/login'
    def get_queryset(self) :
        return self.request.user.notes.all()



class UserProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'profile_edit.html' 
    success_url = '/profile' 

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        else:
            context['profile_form'] = ProfileForm(instance=self.request.user.profile)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        if profile_form.is_valid():
            form.save()
            profile_form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
  

# Create your views here.
