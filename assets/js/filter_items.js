function filter_items(){
    // const search_query = document.getElementById('search-query-field').value
    const brend = Array()
    document.querySelectorAll('.cheked').forEach(function(elem) {
        if (elem.checked == true){
            brend.push(elem.value);
        }
    });
    
    const search = document.getElementById('search-query-field').value
    const price_min = document.getElementById('range-min').value
    const price_max = document.getElementById('range-max').value
    const category = getParameterByName('category')
    const bad = getParameterByName('bad')
    const urlParams = new URLSearchParams('')
    
    urlParams.set('brend', brend)
    urlParams.set('search', search)
    urlParams.set('price-min', price_min)
    urlParams.set('price-max', price_max)
    if (category !== null){
    urlParams.set('category', category)
    }
    if (bad !== null){
    urlParams.set('bad', bad)
    }
    window.location.search = urlParams

}



// prefilling search fields
document.addEventListener("DOMContentLoaded", function() {
  fill_search_fields()

})

function fill_search_fields(){
  
  if(getParameterByName('search') != null){
    document.getElementById('search-query-field').value = getParameterByName('search')
  }

  if(getParameterByName('price-min') != null){
    min_price = getParameterByName('price-min')
    
    document.getElementById('range-min').value = min_price
    document.getElementById('price-min').value = min_price
    range.style.left = (min_price / rangeInput[0].max) * 100 + "%";
}
if(getParameterByName('price-max') != null){
    max_price = getParameterByName('price-max')
    
    document.getElementById('range-max').value = max_price
    document.getElementById('price-max').value = max_price
    range.style.right = 100 - (max_price / rangeInput[1].max) * 100 + "%";
}
  
if(getParameterByName('brend') != null){
    brends = getParameterByName('brend').split(',')
    for (let brend of brends){
        console.log(brend)
        document.getElementById('brend-' + brend).checked = true
    }
  }
} 

