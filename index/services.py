from django.contrib.sessions.models import Session

from django.db.models import Q

from items.models import Item, Cart
from badshop_django.logger import logger

def get_filter_items(max_item_price, query, brend, category, bad, price_max, price_min):

    filter_dict = {}
    q_objects = Q()
    if category:
        filter_dict['category__id__in'] = category

    if brend and brend != ['']:
        filter_dict['brend__id__in'] = brend
    
    # active_substance  
    if bad and bad != ['']:
        filter_dict['active_bad__id'] = bad
    
    if query:
        q_objects |= Q(name__icontains=query)
        q_objects |= Q(brend__name__icontains=query)
        q_objects |= Q(category__title__icontains=query)
        q_objects |= Q(active_bad__title__icontains=query)
    
    items = Item.objects.filter(
        q_objects,
        price__range=(price_min, price_max),
        **filter_dict
    )

    return items

