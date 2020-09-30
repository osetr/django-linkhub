obj = new Vue({
    el: '#show_playlists',
    delimiters: ["[[", "]]"],
    data:{
        opacity: [],
        show: false
    },
    methods: {
        save_to_clickboard(pk)
        {
            $.ajax({
                type: 'GET',
                async: false,
                url: url_private_link + pk,
                success: function(data) {
                    str = data['response']
                },
                dataType: 'json',
            });
            const el = document.createElement('textarea');
            el.value = '127.0.0.1:8000' + url_show_playlist + str;
            el.setAttribute('readonly', '');
            el.style.position = 'absolute';
            el.style.left = '-9999px';
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            this.show = true;
        },
        repeat_check(pk){
            $.ajax({
                type: 'GET',
                async: false,
                url: url_check_alive + pk,
                success: function(data) {
                    if (data['response'] == 'success')
                    {
                        op = data['blur']
                    }
                    else{
                        op = 0
                    }
                },
                dataType: 'json',
            });
            this.opacity.push({pk:1});
            this.opacity[pk] = op
        },
        check_alive(pk){
            this.opacity.push({pk:1});
            this.opacity[pk] = 1
            setInterval(this.repeat_check, 1000, pk);
        },
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