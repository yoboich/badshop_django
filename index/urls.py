from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetCompleteView, PasswordResetConfirmView
)

from blog.views import blog, blogPage
from index.views import index, catalog_categories, item, brends, pay, sail, salePage, about, partners, \
    contacts, cabinet, cart, my_data, myadress, \
    delete_address, edit_myaddress, favorite, CustomUserPasswordChangeView, toggle_favorites, toggle_cart, \
    get_cart_count, filter_catalog_view
from orders.views import (
    update_cart_ajax, get_item_data_ajax, 
    toggle_item_active_state_ajax, 
    get_cart_data_ajax, 
    payment_finished_view, order_page_view,
    save_order_data_view
    )
from users.views import AppLoginView, AppLogoutView, AppRegistration
from users.forms import CustomUserSetPasswordForm
from items.views import toggle_item_favorite_state_ajax, get_favorite_total_count_ajax
from utils.views import yoo_kassa_webhook_view

urlpatterns = [

    # ГЛАВНАЯ СТРАНИЦА
    path('', index, name="index"),

    # КАТАЛОГ
    path('catalog/', catalog_categories, name="catalog_categories"),
    path('catalog/category/item/<item_id>/', item, name="item"),
    path('catalog/filter/', filter_catalog_view, name='filter_catalog_view'),


    path('brends/', brends, name="brends"),
    path('pay/', pay, name="pay"),
    path('sale/', sail, name="sail"),
    path('sale/<sale_id>/', salePage, name="salePage"),

    # АУТЕНТИФИКАЦИЯ
    path('login/', AppLoginView.as_view(), name="login"),
    path('logout/', AppLogoutView.as_view(), name="logout"),
    path('registration/', AppRegistration.as_view(), name="registration"),

    path('password_reset/', PasswordResetView.as_view(success_url = reverse_lazy('password_reset_done')), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(
             form_class=CustomUserSetPasswordForm, 
             success_url = reverse_lazy('password_reset_complete')
             ), 
             name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # БЛОГ
    path('blog/', blog, name="blog"),
    path('blog/<post_id>/', blogPage, name="blogPage"),

    # ОСТАЛЬНЫЕ СТРАНИЦА
    path('about/', about, name="about"),
    path('partners/', partners, name="partners"),
    path('contacts/', contacts, name="contacts"),

    # ЛИЧНЫЙ КАБИНЕТ
    path('cabinet/', cabinet, name="cabinet"),
    path('cabinet/my_data/', my_data, name="my_data"),
    path('cabinet/reset_password/', CustomUserPasswordChangeView.as_view(), name="reset_password"),
    path('cabinet/my_adress/', myadress, name="myadress"),
    path('cabinet/my_adress/delete_address/<int:address_id>/', delete_address, name='delete_address'),
    path('cabinet/my_adress/edit_myaddress/<int:address_id>/', edit_myaddress, name='edit_myaddress'),
    path('cabinet/favorite/', favorite, name='favorite'),

    # КОРЗИНА
    path('cart/', cart, name="cart"),
    path('update_cart/', update_cart_ajax, name='update_cart'),
    path('toggle_item_active_state/', toggle_item_active_state_ajax, name='toggle_item_active_state'),
    path('get_cart_data/', get_cart_data_ajax, name='get_cart_data'),

    # РАБОТА С КАРЗИНОЙ И ИЗБРАННЫМИ
    path('get_cart_count/', get_cart_count, name="get_cart_count"),
    path('get_favorite_total_count/', get_favorite_total_count_ajax, name="get_favorite_total_count"),
    path('toggle_cart/<int:item_id>/', toggle_cart, name='toggle_cart'),
    path('toggle_favorites/<int:item_id>/', toggle_favorites, name='toggle_favorites'),
    path('get_item_data/', get_item_data_ajax, name='get_item_data'),
    path('toggle_item_favorite_state/', toggle_item_favorite_state_ajax, name='toggle_item_favorite_state'),

    path('order_page/', order_page_view, name='order_page'),
    path('payment_finished/', payment_finished_view, name='payment_finished'),
    path('save_order_data/', save_order_data_view, name='save_order_data'),

    path('webhooks/yookassa/', yoo_kassa_webhook_view, name='yoo_kassa_webhook'),

]