from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from items.models import CartItem, Cart, Item
from items.services import get_or_create_cart, get_cart_data


# желательно разделить
def update_cart_ajax(request):
    quantity = int(request.POST.get('quantity'))
    item_id = request.POST.get('item_id')
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity = quantity
    cart_item.save()

    cart_data = get_cart_data(request)
    cart_data.update({'success': 'success'})
    cart_data.update(
        {'total_cart_item_price_with_discount': \
         cart_item.total_price_with_discount()}
         )
    print(cart_data)
    return JsonResponse(cart_data)
    

def toggle_item_active_state_ajax(request):
    cart_item_id = request.POST.get('cart_item_id')
    state = True if request.POST.get('state') == 'true' else False
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.is_active = state
    cart_item.save()

    return JsonResponse({'success':'success'})


def get_cart_data_ajax(request):
    cart_data = get_cart_data(request)
    print(cart_data)
    return JsonResponse(cart_data)


# для модалки при добавлении продукта в корзину
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



