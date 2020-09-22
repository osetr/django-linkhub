obj = new Vue({
    el: '#show_playlists',
    delimiters: ["[[", "]]"],
    methods: {
        like(playlist_id) {
            $.ajax({
                type: 'GET',
                async: true,
                url: url_like + playlist_id,
                success: function(data) {
                    document.getElementById('like' + playlist_id + '_amount').innerHTML=data['likes_amount'];
                    document.getElementById('dislike' + playlist_id + '_amount').innerHTML=data['dislikes_amount'];
                },
                dataType: 'json',
            });
        },
        dislike(playlist_id){
            $.ajax({
                type: 'GET',
                async: true,
                url: url_dislike + playlist_id,
                success: function(data) {
                    document.getElementById('like' + playlist_id + '_amount').innerHTML=data['likes_amount'];
                    document.getElementById('dislike' + playlist_id + '_amount').innerHTML=data['dislikes_amount'];
                },
                dataType: 'json',
            });
        },
        inherite_playlist(playlist_id){
            $.ajax({
                type: 'GET',
                async: true,
                url: url_inherite + playlist_id,
                success: function(data) {
                    console.log(data['response'])
                  if (data['response'] == 'inhereted successfuly'){
                    document.getElementById("inherite_playlist" + playlist_id).innerHTML='<img src="https://img.icons8.com/flat_round/23/000000/star--v1.png"/>'
                  }
                  else {
                    document.getElementById("inherite_playlist" + playlist_id).innerHTML='<img src="https://img.icons8.com/ios/16/000000/star.png"/>'
                  }
                },
                dataType: 'json',
            });
        }
    }
    });