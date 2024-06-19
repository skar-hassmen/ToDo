from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import auth
from .forms import UserRegisterForm, AuthUserForm, EmailPasswordResetForm, UserPasswordResetForm


class UserPasswordResetView(PasswordResetView):
    form_class = EmailPasswordResetForm
    template_name = 'users/reset_pass.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/reset_pass_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserPasswordResetForm
    template_name = 'users/reset_pass_confirm.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/reset_pass_complete.html'


class LoginUserView(LoginView):
    form_class = AuthUserForm
    success_url = reverse_lazy('profile')
    template_name = 'users/login.html'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/reg.html'


def logout_user(request):
    auth.logout(request)
    return redirect('/')
