from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q, Min, Max, F, Sum

from balance.models import BonusWallet
from users.forms import UserUpdateForm, AddressForm, AddressEditForm, CustomUserSetPasswordForm
from items.models import *
from users.models import Address
from .models import *
from blog.models import *
from django.contrib.auth.forms import PasswordChangeForm  # Добавьте импорт формы смены пароля
from django.contrib.auth import update_session_auth_hash  # Добавьте импорт для обновления сессии после смены пароля
from django.contrib.auth.views import PasswordChangeView
from unidecode import unidecode
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
# Create your views here.

# GLOBAL CONSTANTS
ITEMS = Item.objects.all()
CATEGORIES = Category.objects.all()
SALES = Sale.objects.all()
SLIDER1 = SliderTop.objects.all()
SLIDER2 = SliderTwo.objects.all()
BRENDS = Brend.objects.all()
POSTS = Post.objects.all()



# СТРАНИЦА ИЗБРАННЫЕ
def favorite(request):
    items = []

    if request.user.is_authenticated:
        # Если пользователь авторизован, получаем товары из базы данных
        cart_item_ids = CartItem.objects.filter(user=request.user).values_list('item_id', flat=True)
        cart_items = list(cart_item_ids)
        favorite_items_ids = FavoriteItem.objects.filter(user=request.user).values_list('item_id', flat=True)
        favorite_items = list(favorite_items_ids)
    else:
        # Если пользователь не авторизован, получаем товары из сессии
        cart_items = request.session.get('cart', [])
        favorite_items = request.session.get('favorites', [])


    if request.user.is_authenticated:
        items = FavoriteItem.objects.filter(user=request.user)

    elif 'favorites' in request.session:
        item_ids = request.session['favorites']
        items = Item.objects.filter(id__in=item_ids)

    context = {
        'title': 'Избранные',
        'items': items,
        'cart_items': cart_items,
        'favorite_items': favorite_items,
    }
    return render(request, 'cabinet/favorite.html', context)

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
        return JsonResponse({'count': cart_count})
    else:
        session_cart = request.session.get('cart', [])
        print(f"session_cart: {session_cart}")  # добавить отладочный вывод
        if isinstance(session_cart, list):  # проверка, что session_cart - это список
            cart_count = len(session_cart)  # считает количество элементов в списке
        else:
            cart_count = 0
        return JsonResponse({'count': cart_count})

def get_favorite_count(request):
    if request.user.is_authenticated:
        favorites_count = FavoriteItem.objects.filter(user=request.user).count()
        return JsonResponse({'count': favorites_count})
    else:
        session_favorites = request.session.get('favorites', [])
        print(f"session_favorites: {session_favorites}")  # добавить отладочный вывод
        if isinstance(session_favorites, list):  # проверка, что session_cart - это список
            favorites_count = len(session_favorites)  # считает количество элементов в списке
            print(favorites_count)
        else:
            favorites_count = 0
        return JsonResponse({'count': favorites_count})

# СТРАНИЦА КОРЗИНЫ


def cart(request):
    cart = None
    total_quantity = 0
    total_discount = 0
    total_without_discount = 0
    total = 0
    bonus_wallet = 0

    def calculate_cart_total(cart):
        total = 0
        for cart_item in cart.items.all():
            total += cart_item.quantity * cart_item.item.seil_price
        return total

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_quantity = sum([cart_item.quantity for cart_item in cart.items.all()])
            total = calculate_cart_total(cart)

            # Получаем объект BonusWallet, связанный с текущим пользователем (предполагая, что пользователь аутентифицирован)
            bonus_wallet = BonusWallet.objects.get(user=request.user).balance

            total_discount = 0
            for cart_item in cart.items.all():
                total_discount += (cart_item.item.price - cart_item.item.seil_price) * cart_item.quantity

            total_without_discount = 0
            for cart_item in cart.items.all():
                total_without_discount += cart_item.item.price * cart_item.quantity
        except Cart.DoesNotExist:
            cart = None


    elif 'cart' in request.session:
        item_ids = request.session['cart']
        cart_items = Item.objects.filter(id__in=item_ids)
        cart = cart_items
        total_quantity = sum([1 for _ in cart_items])

        if cart_items:
            total_discount = 0
        else:
            total_discount = 0

        total_without_discount = 0


        for cart_item in cart_items:
            print(cart_item)
            total_discount += (cart_item.price - cart_item.seil_price) * 1
            total_without_discount += cart_item.price * 1
            total = total_without_discount - total_discount


    context = {
        'cart': cart,
        'title': 'Корзина',
        'total_quantity': total_quantity,
        'total_discount': total_discount,
        'total_without_discount': total_without_discount,
        'total_with_discount': total_without_discount - total_discount,
        'total': total,
        'balance': bonus_wallet,
    }

    return render(request, 'cart/cart.html', context)


# ФИЛЬТРАЦИЯ КАТАЛОГА
def filter(request, category_id=None, items_id=None):
    items = Item.objects.all()
    brends = Brend.objects.all()
    minMaxPrice = Item.objects.aggregate(Min('seil_price'), Max('seil_price'))

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

    if category_id:
        category = Category.objects.get(id=category_id)

        # Получение параметров из GET-запроса
        brend = request.GET.getlist("brend")
        min_price = float(request.GET.get("min_price", 0))
        max_price = float(request.GET.get("max_price", 999999))
        search_query = request.GET.get("search", "")

        if brend:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(brend__id__in=brend) & Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price))
        else:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price))

        context = {
            'category': category,
            'items': items,
            'brends': brends,
            'minMaxPrice': minMaxPrice,
            'cart_items': cart_items,
            'favorite_items': favorite_items,
        }

        return render(request, 'index/catalogpage_filter.html', context)

    if items_id:
        category = Category.objects.get(id=category_id)
        items = Item.objects.filter(id=items_id)
        # Получение параметров из GET-запроса
        brend = request.GET.getlist("brend")
        min_price = float(request.GET.get("min_price", 0))
        max_price = float(request.GET.get("max_price", 999999))
        search_query = request.GET.get("search", "")

        if brend:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(brend__id__in=brend) & Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price))
        else:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price))

        context = {
            'category': category,
            'items': items,
            'brends': brends,
            'minMaxPrice': minMaxPrice,
            'cart_items': cart_items,
            'favorite_items': favorite_items,
        }

        return render(request, 'index/catalogpage_filter.html', context)

    else:
        # Получение параметров из GET-запроса
        brend = request.GET.getlist("brend")
        min_price = float(request.GET.get("min_price", 0))
        max_price = float(request.GET.get("max_price", 999999))
        search_query = request.GET.get("search", "")

        if brend:
            # Фильтр результатов поиска по бренду и цене
            items = items.filter(
                Q(name__iexact=search_query) & Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price) & Q(
                    category__title__iexact=search_query) & Q(brend__id__in=brend) & Q(seil_price__gte=min_price) & Q(
                    seil_price__lte=max_price)
            )
        else:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(name__iexact=search_query) & Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price)
            )

        context = {
            'items': items,
            'brends': brends,
            'minMaxPrice': minMaxPrice,
            'search_query': search_query,
            'cart_items': cart_items,
            'favorite_items': favorite_items,
        }

        return render(request, 'index/catalogpage_filter_search.html', context)



# def cart(request):
#     items = []
#
#     def calculate_cart_total(cart_items):
#         total = 0
#         for item in cart_items:
#             total += item.quantity * item.item.seil_price  # Используйте цену товара со скидкой (seil_price)
#         return total
#
#     if request.user.is_authenticated:
#         items = CartItem.objects.filter(user=request.user)
#
#     elif 'cart' in request.session:
#         item_ids = request.session['cart']
#         items = Item.objects.filter(id__in=item_ids)
#
#     total = calculate_cart_total(items)  # Вычислить общую сумму товаров в корзине
#
#     # Вычислить общее количество товаров в корзине
#     total_quantity = items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
#
#     # Вычислить общую сумму скидки на все товары
#     total_discount = items.aggregate(total_discount=Sum(F('item__price') - F('item__seil_price') * F('quantity')))['total_discount'] or 0
#
#     # Вычислить общую сумму товаров без скидки
#     total_without_discount = items.aggregate(total_without_discount=Sum(F('item__price') * F('quantity')))['total_without_discount'] or 0
#
#     context = {
#         'items': items,
#         'title': 'Корзина',
#         'total': total,  # Добавьте общую сумму в контекст
#         'total_quantity': total_quantity,
#         'total_discount': total_discount,
#         'total_without_discount': total_without_discount,
#     }
#     return render(request, 'cart/cart.html', context)

def update_cart_quantity(request, item_id, new_quantity):


    item = get_object_or_404(Item, pk=item_id)

    # Получите или создайте объект CartItem для текущего пользователя
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)

    if new_quantity <= 0:
        # Если новое количество товара равно или меньше нуля, удалите товар из корзины
        cart_item.delete()
    else:
        # Обновите количество товара в корзине
        cart_item.quantity = new_quantity
        cart_item.save()

    # Пересчитайте обновленные данные корзины
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = calculate_cart_total(cart_items)  # Пересчитать общую стоимость корзины
    total_quantity = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0  # Пересчитать общее количество товаров
    total_discount = calculate_cart_discount(cart_items)  # Пересчитать общую сумму скидки
    total_without_discount = calculate_cart_total_without_discount(cart_items)  # Пересчитать общую сумму товаров без скидки

    # Верните обновленные данные в формате JSON
    data = {
        'message': 'Количество товара обновлено успешно',
        'new_quantity': new_quantity,
        'total_items': total_quantity,
        'total_price': total_price,
        'total_discount': total_discount,
        'total_without_discount': total_without_discount,
    }
    return JsonResponse(data)

# def toggle_cart(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     if request.user.is_authenticated:
#         cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
#         if created:
#             message = 'Товар добавлен в корзину'
#         else:
#             cart_item.delete()
#             message = 'Товар удален из корзины'
#     else:
#         cart = request.session.get('cart', [])
#
#         if item_id not in cart:
#             cart.append(item_id)
#             message = 'Товар добавлен в корзину'
#         else:
#             cart.remove(item_id)
#             message = 'Товар удален из корзины'
#
#     return JsonResponse({'message': message})

# def toggle_cart(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     message = ''
#
#     if request.user.is_authenticated:
#         try:
#             cart = Cart.objects.get(user=request.user)
#         except Cart.DoesNotExist:
#             cart = Cart(user=request.user)
#             cart.save()
#
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
#         if created:
#             message = 'Товар добавлен в корзину'
#         else:
#             cart_item.delete()
#             message = 'Товар удален из корзины'
#     else:
#         cart = request.session.get('cart', [])
#         if item_id not in cart:
#             cart.append(item_id)
#             message = 'Товар добавлен в корзину'
#         else:
#             cart.remove(item_id)
#             message = 'Товар удален из корзины'
#         request.session['cart'] = cart
#
#     return JsonResponse({'message': message})


## ДОБАВЛЕНИЕ ТОВАРОВ В КОРЗИНУ
def toggle_cart(request, item_id):
    if request.user.is_authenticated:
        user = request.user
        session = None
        try:
            # Попробуйте найти существующую корзину для пользователя
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            # Если корзина не существует, создайте новую
            cart = Cart(user=user)
            cart.save()

        try:
            item = Item.objects.get(id=item_id)

            # Попробуйте найти CartItem с соответствующим товаром и корзиной
            try:
                cart_item = CartItem.objects.get(item=item, cart=cart)
                cart.items.remove(cart_item)  # Удаляем товар из корзины
                cart_item.delete()  # Удаляем cart_item
                message = "Товар удален из корзины."
            except CartItem.DoesNotExist:
                cart_item = CartItem(item=item)
                cart_item.save()
                cart.items.add(cart_item)  # Добавляем товар в корзину
                message = "Товар добавлен в корзину."

        except Item.DoesNotExist:
            return JsonResponse({'message': 'Товар не найден.'})

    else:
        cart = request.session.get('cart', [])

        if item_id not in cart:
            cart.append(item_id)
            message = 'Товар добавлен в корзину'
        else:
            cart.remove(item_id)
            message = 'Товар удален из корзины'


        request.session['cart'] = cart


    return JsonResponse({'message': message})



# def toggle_cart(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     if request.user.is_authenticated:
#         cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
#         if created:
#             message = 'Товар добавлен в корзину'
#         else:
#             cart_item.delete()
#             message = 'Товар удален из корзины'
#     else:
#         cart = request.session.get('cart', [])
#         if item_id not in cart:
#             cart.append(item_id)
#             message = 'Товар добавлен в корзину'
#         else:
#             cart.remove(item_id)
#             message = 'Товар удален из корзины'
#         request.session['cart'] = cart
#
#     return JsonResponse({'message': message})

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
        'items_sails': ITEMS.filter(discount__gt=0),
        'categories': Category.objects.all(),
        'slider1': SliderTop.objects.all(),
        'slider2': SliderTwo.objects.all(),
        'popular_items': Item.objects.all().order_by('-rating'),
        'brends': Brend.objects.all(),
        'cart_items': cart_items,
        'favorite_items': favorite_items,
    }
    return render(request, 'index/index.html', context)



# КАТАЛОГ
def catalog(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
    }
    return render(request, 'index/catalog.html', context)


# СТРАНИЦА КАТЕГОРИИ КАТАЛОГА
def catalog_page(request, category_id):
    categories = Category.objects.all()
    minMaxPrice = Item.objects.aggregate(Min('seil_price'), Max('seil_price'))
    minPrice = Item.objects.aggregate(Min('seil_price'))['seil_price__min']
    category = categories.get(id=category_id)
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
        'category': category,
        'items': Item.objects.filter(category_id=category_id),
        'categories': categories,
        'brends': Brend.objects.all(),
        'minMaxPrice': minMaxPrice,
        'minPrice': minPrice,
        'title': f'{category.title}',
        'cart_items': cart_items,
        'favorite_items': favorite_items,
    }
    return render(request, 'index/catalogpage.html', context)




# СТРАНИЦА ТОВАРА
def item(request, item_id):
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

    items = Item.objects.all()
    item = items.get(id=item_id)
    context = {
        'item': items.get(id=item_id),
        'items': items,
        'certificates': CertificateImages.objects.filter(item=item),
        'title': f'{item.name}',
        'cart_items': cart_items,
        'favorite_items': favorite_items,
    }
    return render(request, 'index/item.html', context)

# СТРАНИЦА - БРЕНДЫ
def brends(request):
    context = {
        'brends': Brend.objects.all(),
        'title': 'Бренды'
    }
    return render(request, 'index/brends.html', context)


def pay(request):
    context = {'title': 'Оплата и доставка',}
    return render(request, 'index/pay.html', context)


# СТРАНЦИА АКЦИИ
def sail(request):
    context = {
        'sales': Sale.objects.all(),
        'title': 'Акции',
    }
    return render(request, 'index/sail.html', context)


# СТРАНИЦА ОПРЕДЕЛЕННОЙ АКЦИИ
def salePage(request, sale_id):
    sale = Sale.objects.all().get(id=sale_id)
    context = {
        'sale': sale,
        'title': f'{sale.title}',
    }
    return render(request, 'index/sailpage.html', context)


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
            address = Address.objects.filter(users=request.user)
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



# @login_required
# def add_to_favorites(request, item_id):
#     item = get_object_or_404(Item, pk=item_id)
#     favorite, created = FavoriteItem.objects.get_or_create(user=request.user, item=item)
#     if created:
#         return JsonResponse({'status': 'added'})
#     else:
#         return JsonResponse({'status': 'already_exists'})

