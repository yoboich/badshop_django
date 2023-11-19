from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from items.models import CartItem, Cart, Item
from index.services import get_or_create_cart


def update_cart_ajax(request):
    quantity = int(request.POST.get('quantity'))
    item_id = request.POST.get('item_id')
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity = quantity
    cart_item.save()

    cart = get_or_create_cart(request)

    total_items_count = cart.total_quantity()
    discount = cart.total_discount()
    total_price = cart.total_price()
    total_cart_item_price_with_discount = cart_item.total_price_with_discount()
    total_price_without_discount = cart.items_price_without_discount()
    distinct_items_count = cart.cartitem_set.count()

    return JsonResponse({
        'success': 'success',
        'total_items_count': total_items_count,
        'total_price_without_discount': total_price_without_discount,
        'discount': discount,
        'total_price': total_price,
        'total_cart_item_price_with_discount': total_cart_item_price_with_discount,
        'distinct_items_count': distinct_items_count,
        })
    

def get_item_data_ajax(request):
    item_id = request.GET.get('item_id')
    print(item_id)
    item = Item.objects.get(id=item_id)
    cart = get_or_create_cart(request)
    cart_item = CartItem.objects.get(
        item=item,
        cart=cart)
    
    rendered_item = render_to_string(
        'cart/__item_added_render.html', 
        {'item': cart_item}
        )
    
    return JsonResponse({'success': rendered_item})