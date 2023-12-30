import sys
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login as auth_login

from items.services import get_current_session
from items.models import Cart
from users.forms import LoginForm, CustomUserCreationForm
from users.services import (
    transfer_items_from_session_to_user_cart,
    transfer_items_from_session_to_user_favorites
)
from badshop_django.logger import logger
logger.debug(f'server is - {sys.argv}')
# Create your views here.

from django.utils.regex_helper import _lazy_re_compile
import django.http.request

django.http.request.host_validation_re = _lazy_re_compile(r"[a-zA-z0-9.:]*")

class AppLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_valid(self, form):
        """Переносим предметы корзины из сессии юзеру"""
        transfer_items_from_session_to_user_cart(self.request)
        transfer_items_from_session_to_user_favorites(self.request)
        auth_login(self.request, form.get_user())
        
        return HttpResponseRedirect(self.get_success_url())

    redirect_authenticated_user = True

class AppRegistration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('cabinet')


    def form_valid(self, form):
        response = super().form_valid(form)
        transfer_items_from_session_to_user_cart(self.request)
        transfer_items_from_session_to_user_favorites(self.request)
        auth_login(self.request, self.object)  # Use auth_login instead of login
        return response

class AppLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')