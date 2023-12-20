

function toggle_favorite(item_id){
    $.ajax({
        type: 'POST',
        url: toggle_favorite_url,
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: {
            item_id: item_id
        },
        success: function(json){
            
            const btn_fav_main = document.getElementById('add-favorite-item')
            const btn_fav_suggestions = document.getElementById('button-add-to-favorites-' + item_id)
            if (json['created'] === true){
                btn_fav_main.innerHTML = 'В избранном'
                
                btn_fav_suggestions.classList.add('item-favorited');
            }else{
                btn_fav_main.innerHTML = 'Добавить в избранное'
                btn_fav_suggestions.classList.remove('item-favorited');
            }
            update_favorite_total_count()
        }
    })
}



// Получаем количество избранных товаров для навбара
function update_favorite_total_count() {
    $.ajax({
        type: 'GET',
        url: favorite_total_count_url,
        success: function(json){
            document.getElementById('like-count').innerHTML= json['favorite_total_count']
        }
        
    })

}