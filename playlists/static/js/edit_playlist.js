obj = new Vue({
    delimiters: ["[[", "]]"],
    el: '#edit_playlist',
    data: {
        newLink: '',
        todos: [],
        nextTodoId: 1,
        playlist_deleted: playlist_deleted
    },
    methods: {
        addNewLink: function () {
          this.todos.push({
              id: this.nextTodoId++,
              link: this.newLink,
              description: '',
              check: false,
          })
          this.newLink = ''
        },

        deleteLink(val) {
          for (var i = 0; i < this.todos.length; i++)
            if (this.todos[i].id === val) 
            {
                this.todos.splice(i,1);
                break;
            }
        },

        remove_playlist: function() {
          $.ajax({
              vue: this,
              type: 'GET',
              async: true,
              url: url_remove_playlist,
              success: function(data) {
                if (data['response'] == 'success'){
                  this.vue.playlist_deleted = true
                }
              },
              dataType: 'json',
          });
        },

        restore_playlist: function() {
          $.ajax({
              vue: this,
              type: 'GET',
              async: true,
              url: url_restore_playlist,
              success: function(data) {
                if (data['response'] == 'success'){
                  this.vue.playlist_deleted = false
                }
              },
              dataType: 'json',
          });
        }
    },
    computed: {
      all_links: function() {
        var result = [];
        for (var i = 0; i < this.todos.length; i++)
            result.push("\
              link:" + this.todos[i].link + ",\
              description:" + this.todos[i].description + ",\
              check:" + this.todos[i].check + ",\
            ");
        return result
      }
    }
    })