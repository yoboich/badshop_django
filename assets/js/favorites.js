

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
            const fav_btns = document.querySelectorAll(`[data-like-item-id="${item_id}"]`);
         
            if (json['created'] === true){
                if (btn_fav_main !== null){
                    btn_fav_main.innerHTML = 'В избранном'
                }
                fav_btns.forEach((btn) => {
                    btn.classList.add('item-favorited');
                })
            }else{
                if (btn_fav_main !== null){
                    btn_fav_main.innerHTML = 'Добавить в избранное'
                }
                fav_btns.forEach((btn) => {
                    btn.classList.remove('item-favorited');
                })
                console.log(window.location.href)
                if (window.location.href.includes('cabinet/favorite')){
                    document.getElementById('item-' + item_id).hidden = true
                }
            }
            update_favorite_total_count()
        }
    })
}



// Получаем количество избранных товаров для навбара
function update_favorite_total_count() {
    likeCountElement = document.getElementById('like-count')
    $.ajax({
        type: 'GET',
        url: favorite_total_count_url,
        success: function(json){
            let count = json['favorite_total_count']
            if (count > 0){
                likeCountElement.innerHTML = count
                likeCountElement.hidden = false
            }else{
                likeCountElement.hidden = true
            }
        }
        
    })

}