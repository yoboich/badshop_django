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
      item_id = e.target.id.split('-')[1]
      update_cart(val, item_id)
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
    console.log('!here')

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
                  document.getElementById('total-quantity').innerText = json['total_items_count']
                  document.getElementById('total-price-without-discount').innerText = json['total_price_without_discount']
                  document.getElementById('total-discount').innerText = json['discount']
                  document.getElementById('total-price').innerText = json['total_price']
            }else if ('error' in json){

            }else{
                alert('Что-то пошло не так!')
            }
        }
    })
}