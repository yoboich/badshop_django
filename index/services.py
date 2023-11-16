from django.db.models import Q

from items.models import Item

def get_filter_items(max_item_price, query, brend, price_max, price_min):

    filter_dict = {}
    q_objects = Q() 
    
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