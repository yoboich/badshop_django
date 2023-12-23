from django.urls import path

from blog.views import blog, blogPage
from index.views import index, catalog_categories, item, brends, pay, sail, salePage, about, partners, \
    contacts, cabinet, cart, my_data, myadress, \
    delete_address, edit_myaddress, favorite, CustomUserPasswordChangeView, toggle_favorites, toggle_cart, \
<<<<<<< HEAD
    get_cart_count, update_cart_quantity, filter_catalog_view, order
from orders.views import update_cart_ajax, get_item_data_ajax, toggle_item_active_state_ajax, get_cart_data_ajax
=======
    get_cart_count, update_cart_quantity, filter_catalog_view
from orders.views import (
    update_cart_ajax, get_item_data_ajax, 
    toggle_item_active_state_ajax, 
    get_cart_data_ajax, make_payment_view,
    payment_success_view
    )
>>>>>>> 13a4d2c (creating order)
from users.views import AppLoginView, AppLogoutView, AppRegistration
from items.views import toggle_item_favorite_state_ajax, get_favorite_total_count_ajax

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
    path('update_quantity/<int:item_id>/<int:new_quantity>/', update_cart_quantity, name='update_quantity'),
    path('get_item_data/', get_item_data_ajax, name='get_item_data'),
    path('toggle_item_favorite_state/', toggle_item_favorite_state_ajax, name='toggle_item_favorite_state'),
<<<<<<< HEAD
    path('order/', order, name="order")
=======

    path('make_payment/', make_payment_view, name='make_payment'),
    path('payment_success/', payment_success_view, name='payment_success'),
>>>>>>> 13a4d2c (creating order)
]