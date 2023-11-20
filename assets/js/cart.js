$(document).on('DOMContentLoaded', function () {
  console.log('!!hey')
  $('body').on('click', '.number-minus, .number-plus', function (e) {
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
    if (val > 0) {
      item_id = e.target.id.split('-')[1]
      item_quantity = document.getElementById('item-quantity')
      if (item_quantity !== null) {
        item_quantity.innerText = val
      }
      update_cart(val, item_id)
    }

   
  });
  $('body').on('change', '.number-text', function () {
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
// Находим элементы формы
  var selectAllCheckbox = document.getElementById('select-all');
  var checkboxes = document.querySelectorAll('input[name="cart-item-active"]');

  // Привязываем обработчик события "click" к флажку "выбрать все"
  selectAllCheckbox.addEventListener('click', function(event) {
    var promises = []
    for (let cb of checkboxes) {
      cb.checked = selectAllCheckbox.checked;
      promises.push(toggle_cart_item_active_state(cb.id.split('-')[3], cb.checked, false))
    }
   Promise.all(promises)
   .then(responseList => {
    get_cart_data()
   })

  });
  for (let cb of checkboxes){
    cb.addEventListener('change', ()=>{
      toggle_cart_item_active_state(cb.id.split('-')[3], cb.checked, true)
    })
  }


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
              fill_cart_data(json)
            }else if ('error' in json){

            }else{
                alert('Что-то пошло не так!')
            }
        }
    })
}

// update_now используем тру если жмем на отдельный выключатель и
// фолс если жмем на общий. Для общего это позволяет дождаться, пока 
// все аджаксы отработают и затем обновить корзину.
function toggle_cart_item_active_state(cart_item_id, state, update_now){
  return $.ajax({
    type: 'POST',
    url: toggle_item_active_state_url,
    headers: {
      'X-CSRFToken': csrfToken
    },
    data: {
      cart_item_id: cart_item_id,
      state: state,
    },
    success: function(json){
      if (update_now){
        get_cart_data(json)
      }
    }
  })
}

function get_cart_data(){
  $.ajax({
    type: 'GET',
    url: get_cart_data_url,
    success: function(json){
        fill_cart_data(json)
    }
  })
}

function fill_cart_data(json){
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
}

