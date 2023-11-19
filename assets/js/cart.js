$(document).ready(function() {
    $('body').on('click', '.number-minus, .number-plus', function(e){
      var $row = $(this).closest('.number');
      var $input = $row.find('.number-text');
      var step = $row.data('step');
      var val = parseFloat($input.val());
      if ($(this).hasClass('number-minus')) {
        val -= step;
      } else {
        val += step;
      }
      $input.val(val);
      $input.change();
      if (val > 0){
      item_id = e.target.id.split('-')[1]
      item_quantity = document.getElementById('item-quantity')
      if (item_quantity !== null){
        item_quantity.innerText = val
      }
      update_cart(val, item_id)
      }
      
      return false;
    });

    $('body').on('change', '.number-text', function(){
      var $input = $(this);
      var $row = $input.closest('.number');
      var step = $row.data('step');
      var min = parseInt($row.data('min'));
      var max = parseInt($row.data('max'));
      var val = parseFloat($input.val());
      if (isNaN(val)) {
        val = step;
      } else if (min && val < min) {
        val = min;
      } else if (max && val > max) {
        val = max;
      }
      $input.val(val);
    });
  });


function update_cart(quantity, item_id){

    $.ajax({
        type: 'POST',
        url: update_cart_url,
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: {
            quantity: quantity,
            item_id: item_id
        },
        success: function(json){
            if ('success' in json){
                  total_quantity = document.getElementById('total-quantity')
                  if (total_quantity !== null){
                    total_quantity.innerText = json['total_items_count']
                  }
                  total_price_without_discount = document.getElementById('total-price-without-discount')
                  if (total_price_without_discount !== null){
                    total_price_without_discount.innerText = json['total_price_without_discount']
                  }
                  total_discount = document.getElementById('total-discount')
                  if(total_discount !== null){
                    total_discount.innerText = json['discount']
                  }
                  total_price = document.getElementById('total-price')
                  if (total_price !== null){
                    total_price.innerText = json['total_price']
                  }
                  total_cart_item_price_with_discount = document.getElementById('total-cart-item-price-with-discount')
                  if (total_cart_item_price_with_discount !== null){
                    total_cart_item_price_with_discount.innerText = json['total_cart_item_price_with_discount']
                  }
                  // item_quantity = document.getElementById('item-quantity')
                  // if (item_quantity !== null){
                  //   item_quantity.innerText = json['item']
                  // }
            }else if ('error' in json){

            }else{
                alert('Что-то пошло не так!')
            }
        }
    })
}