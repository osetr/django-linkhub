obj = new Vue({
    el: '#show_introduction',
    methods: {
        show_intro: function () {
        $.ajax({
            type: 'GET',
            async: true,
            url: url,
            success: function(data) {
            },
            dataType: 'json',
        })
        }
    }
    });