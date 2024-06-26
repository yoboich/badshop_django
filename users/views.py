import sys
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
from items.services.services import get_current_session
from items.models import Cart
from users.forms import LoginForm, CustomUserCreationForm
from users.services import (
    transfer_items_from_session_to_user_cart,
    transfer_items_from_session_to_user_favorites
)
from badshop_django.logger import logger

# Create your views here.



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

# class AppRegistration(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration.html'
#     success_url = reverse_lazy('cabinet')


#     def form_valid(self, form):
#         response = super().form_valid(form)
#         transfer_items_from_session_to_user_cart(self.request)
#         transfer_items_from_session_to_user_favorites(self.request)
#         auth_login(self.request, self.object)  # Use auth_login instead of login
#         return response
class AppRegistration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('cabinet')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Получаем реферральный код из куки
        referral_code = self.request.COOKIES.get('referral_code')

        # Если есть реферральный код, пытаемся найти пригласившего пользователя
        if referral_code:
            try:
                inviter_user = CustomUser.objects.get(referral_code=referral_code)
                self.object.invited_by = inviter_user
                self.object.save()  # Сохраняем изменения в пользователе
            except CustomUser.DoesNotExist:
                pass  # Если пользователь с реферральным кодом не найден, игнорируем
        
        transfer_items_from_session_to_user_cart(self.request)
        transfer_items_from_session_to_user_favorites(self.request)
        auth_login(self.request, self.object)  # Use auth_login instead of login
        
        return response
    

class AppLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')