from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q, Min, Max, F, Sum

from balance.models import BonusWallet
from orders.models import TransportCompany, Order
from users.forms import UserUpdateForm, AddressForm, AddressEditForm, CustomUserSetPasswordForm
from items.models import *
from users.models import Address
from .models import Sale, SliderTop, SliderTwo, Partner
from blog.models import Post
from django.contrib.auth.forms import PasswordChangeForm  # Добавьте импорт формы смены пароля
from django.contrib.auth import update_session_auth_hash  # Добавьте импорт для обновления сессии после смены пароля
from django.contrib.auth.views import PasswordChangeView
from unidecode import unidecode
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from django.urls import reverse
from items.models import FavoriteItem
from blog.models import Paragraph
from .services import get_filter_items

# Create your views here.

# GLOBAL CONSTANTS
ITEMS = Item.objects.all()
CATEGORIES = Category.objects.all()
SALES = Sale.objects.all()
SLIDER1 = SliderTop.objects.all()
SLIDER2 = SliderTwo.objects.all()
BRENDS = Brend.objects.all()
POSTS = Post.objects.all()


def favorite(request):
    
    items = FavoriteItem.get_favorite_items(request)

    context = {
        'title': 'Избранные',
        'items': items,
    }
    return render(request, 'cabinet/favorite.html', context)


def get_cart_count(request):
    cart = Cart.get_or_create_cart(request)
    cart_count = cart.distinct_items_count
    return JsonResponse({'count': cart_count})




# СТРАНИЦА КОРЗИНЫ


def cart(request):
    cart = Cart.get_or_create_cart(request)

    context = {
        'cart': cart,
        'title': 'Корзина',
    }
    return render(request, 'cart/cart.html', context)




## ДОБАВЛЕНИЕ ТОВАРОВ В КОРЗИНУ
def toggle_cart(request, item_id):
    
    cart = Cart.get_or_create_cart(request)
    item = Item.objects.get(id=item_id)

    cart_item = CartItem.objects.filter(cart=cart, item=item)
    if cart_item:
        cart_item.delete()
        message = "Товар удален из корзины."
    else:
        CartItem.objects.create(
            cart=cart,
            item=item,
            quantity=1
        )
        message = "Товар добавлен в корзину."

    return JsonResponse({'message': message})



## ДОБАВЛЕНИЕ ТОВАРОВ В ИЗБРАННОЕ
def toggle_favorites(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user.is_authenticated:
        favorite_item, created = FavoriteItem.objects.get_or_create(user=request.user, item=item)
        if created:
            message = 'Товар добавлен в избранное'
        else:
            favorite_item.delete()
            message = 'Товар удален из избранного'
    else:
        favorites = request.session.get('favorites', [])
        if item_id not in favorites:
            favorites.append(item_id)
            message = 'Товар добавлен в избранное'
        else:
            favorites.remove(item_id)
            message = 'Товар удален из избранного'
        request.session['favorites'] = favorites

    return JsonResponse({'message': message})


# ГЛАВНАЯ СТРАНИЦА
def index(request):

    if request.user.is_authenticated:
        # Если пользователь авторизован, получаем товары из базы данных
        cart_item_ids = CartItem.objects.filter(cart__user=request.user).values_list('item_id', flat=True)
        cart_items = list(cart_item_ids)
        favorite_items_ids = FavoriteItem.objects.filter(user=request.user).values_list('item_id', flat=True)
        favorite_items = list(favorite_items_ids)
    else:
        # Если пользователь не авторизован, получаем товары из сессии
        cart_items = request.session.get('cart', [])
        favorite_items = request.session.get('favorites', [])

    context = {
        'title': 'Главная страница',
        'items_sales': ITEMS.filter(discount__gt=0, hidden=False),
        'categories': Category.objects.all(),
        'slider1': SliderTop.objects.all(),
        'slider2': SliderTwo.objects.all(),
        'popular_items': Item.objects.filter(hidden=False).order_by('-rating'),
        'brends': Brend.objects.all(),
        'cart_items': cart_items,
        'favorite_items': favorite_items,
        'posts': Post.objects.all(),
    }

    return render(request, 'index/index.html', context)



# КАТАЛОГ
def catalog_categories(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
    }
    return render(request, 'index/catalog_categories.html', context)



from .forms import ReviewForm
# СТРАНИЦА ТОВАРА
def item(request, item_slug):
    if request.user.is_authenticated:
        # Если пользователь авторизован, получаем товары из базы данных
        cart_item_ids = CartItem.objects.filter(cart__user=request.user).values_list('item_id', flat=True)
        cart_items = list(cart_item_ids)
        favorite_items_ids = FavoriteItem.objects.filter(user=request.user).values_list('item_id', flat=True)
        favorite_items = list(favorite_items_ids)
    else:
        # Если пользователь не авторизован, получаем товары из сессии
        cart_items = request.session.get('cart', [])
        favorite_items = request.session.get('favorites', [])



    if request.method == 'POST':
        form = ReviewForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review added successfully')
            return redirect(request.META.get('HTTP_REFERER', '/'))  # возвращаем пользователя на предыдущую страницу
        else:
            messages.error(request, f'There was an error adding your review: {form.errors}')
    else:
        form = ReviewForm(request=request)

    items = Item.objects.filter(hidden=False)
    item = items.get(slug=item_slug)
    cart = Cart.get_or_create_cart(request)
    context = {
        'item': items.get(slug=item_slug),
        'items': items,
        'certificates': CertificateImages.objects.filter(item=item),
        'images': ItemImages.objects.filter(item=item),
        'title': f'{item.name}',
        'cart': cart,
        'cart_items': cart_items,
        'favorite_items': favorite_items,
        'ratings': Review.objects.filter(item=item),
        'form': form
    }
        # Проверяем, была ли установлена кука для данного товара
    if not request.COOKIES.get(f'item_{item.id}_viewed'):
        # Если кука не установлена, увеличиваем счетчик просмотров и устанавливаем куку
        item.views_count += 1
        item.save()
        response = render(request, 'index/item.html', context)
        response.set_cookie(f'item_{item.id}_viewed', 'true', max_age=3600)  # Кука действует 1 час

        return response
    return render(request, 'index/item.html', context)

# СТРАНИЦА - БРЕНДЫ
def brends(request):
    context = {
        'brends': Brend.objects.all(),
        'title': 'Бренды'
    }
    return render(request, 'index/brends.html', context)


def pay(request):
    context = {
        'title': 'Оплата и доставка',
        'paragraphs': Paragraph.objects.all()}
    return render(request, 'index/pay.html', context)


# СТРАНЦИА АКЦИИ
def sale(request):
    context = {
        'sales': Sale.objects.all(),
        'title': 'Акции',
    }
    return render(request, 'index/sale.html', context)


# СТРАНИЦА ОПРЕДЕЛЕННОЙ АКЦИИ
def salePage(request, sale_id):
    sale = Sale.objects.all().get(id=sale_id)
    context = {
        'sale': sale,
        'title': f'{sale.title}',
    }
    return render(request, 'index/salepage.html', context)


# СТРАНИЦА О КОМПАНИИ
def about(request):
    context = {'title': 'О  компании',}
    return render(request, 'index/about.html', context)


# СТРАНИЦА ПАРТНЕРЫ
def partners(request):
    context = {
        'partners': Partner.objects.all(),
        'title': 'Партнеры',
    }
    return render(request, 'index/partners.html', context)


# СТРАНИЦА КОНТАКТЫ
def contacts(request):
    context = {'title': 'Контакты',}
    return render(request, 'index/contacts.html', context)


def cabinet(request):
    if request.user.is_authenticated:
        context = {
            'title': 'Мой кабинет',
        }
        return render(request, 'cabinet/cabinet.html', context)
    else:
        return redirect('login')



# СТРАНИЦА МОИ АДРЕСА
def myadress(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddressForm(request.POST, initial={'user': request.user})
            if form.is_valid():
                form.save()
                return redirect('myadress')  # Перенаправление на список адресов после успешного сохранения
        else:
            form = AddressForm(initial={'user': request.user})
            address = Address.objects.filter(user=request.user)
            context = {
                'title': 'Мои адреса',
                'form': form,
                'address': address,
                'address_count': address.count()
            }
        return render(request, 'cabinet/myadress.html', context)
    else:
        return redirect('login')

def delete_address(request, address_id):
    # Получаем адрес по ID или возвращаем 404 ошибку, если адрес не существует
    address = Address.objects.get(pk=address_id)

    # Если запрос выполнен методом POST, удаляем адрес
    address.delete()
    return redirect('myadress')  # Перенаправление на список адресов после удаления



def edit_myaddress(request, address_id):
    # Получаем адрес по ID или возвращаем 404 ошибку, если адрес не существует
    address = get_object_or_404(Address, id=address_id)

    if request.method == 'POST':
        form = AddressEditForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('myadress')  # Перенаправление на список адресов после успешного редактирования
    else:
        form = AddressEditForm(instance=address)

    return render(request, 'cabinet/edit_myadress.html', {'form': form, 'title': address.title})
    


def reset_password(request):

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Обновление сессии после смены пароля
            messages.success(request, 'Пароль успешно изменен.')

            return redirect('my_data')  # Здесь замените 'profile' на имя URL вашего профиля пользователя.

    else:
        password_form = PasswordChangeForm(request.user)


    context = {
        'title': 'Изменение пароля',
        'form': password_form,
        'password_form': password_form,
    }
    return render(request, 'cabinet/reset_password.html', context)


def my_data(request):

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')

            return redirect('my_data')  # Здесь замените 'profile' на имя URL вашего профиля пользователя.
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'title': 'Мои данные',
        'form': form,
    }
    return render(request, 'cabinet/mydata.html', context)


class CustomUserPasswordChangeView(PasswordChangeView):
    form_class = CustomUserSetPasswordForm
    template_name = 'cabinet/reset_password.html'
    success_url = '/cabinet/my_data/'

    def form_valid(self, form):
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


# отображает товары в каталоге с фильтрами и без
def filter_catalog_view(request):
    query = request.GET.get('search')
    brend = request.GET.get('brend')
    bad = int(request.GET.get('bad')) \
        if request.GET.get('bad') else None
    category = int(request.GET.get('category')) \
        if request.GET.get('category') else None
    try:
        brend = list(map(int, brend.split(',')))
    except:
        brend = None
    price_min = request.GET.get('price-min') or 0
    max_item_price = Item.objects.aggregate(
        price_max=Max('price')
        )['price_max']
    
    price_max = request.GET.get('price-max') or max_item_price

    items = get_filter_items(
        max_item_price, query, 
        brend, category, bad,
        price_max, price_min,
        )
    
    cart = Cart.get_or_create_cart(request)
    
    context = {
        'items': items,
        'cart': cart,
        'price_max': max_item_price,
        'brends': Brend.objects.all(),
        'bads': ActiveBad.objects.all().order_by('name'),
        'categories': Category.objects.all()
    }

    return render(request, 'index/catalog_items.html', context)


def historyOrders(request):
    order = Order.objects.filter(user=request.user)
    context = {
        'ordersCount': order.count(),
        'orders':order,
        'title': 'История заказов'
    }
    return render(request, 'cabinet/history_orders.html', context=context)


def MyBonus(request):
    context = {
        'title': 'Мои бонусы',
        'mybonus': BonusWallet.objects.filter(user=request.user)
    }
    return render(request, 'cabinet/my_bonus.html', context=context)

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View


class ReferralLinkView(View):
    def get(self, request, *args, **kwargs):
        referral_code = kwargs.get('referral_code')
        if referral_code:
            # Устанавливаем реферральный код в куки
            response = HttpResponseRedirect(reverse('registration'))
            response.set_cookie('referral_code', referral_code)
            return response
        else:
            # Если реферральный код отсутствует, перенаправляем на страницу по умолчанию
            return redirect('index')