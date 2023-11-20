from django.contrib.sessions.models import Session

from django.db.models import Q

from items.models import Item, Cart

def get_filter_items(max_item_price, query, brend, category, price_max, price_min):

    filter_dict = {}
    q_objects = Q()
    if category:
        filter_dict['category__id__in'] = category

    if brend and brend != ['']:
        filter_dict['brend__id__in'] = brend
        
    if query:
        q_objects |= Q(name__icontains=query)
        q_objects |= Q(brend__name__icontains=query)
        q_objects |= Q(category__title__icontains=query)
    
    items = Item.objects.filter(
        q_objects,
        price__range=(price_min, price_max),
        **filter_dict
    )

    return items

import datetime
from django.utils import timezone

def get_or_create_cart(request):
    cart = []
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if request.session.session_key != None:
            session = Session.objects.get(
                    session_key=request.session.session_key
                    )
            cart, created = Cart.objects.get_or_create(session=session)

    return cart


def get_or_create_session(request):
    if not request.session.session_key is None:
        session = Session.objects.get(
            session_key=request.session.session_key
            )
    else:
        # exp_date = timezone.now() + datetime.timedelta(days=30)
        # session = Session.objects.create(expire_date=exp_date)
        request.session['hey'] = 'hello'
    return request