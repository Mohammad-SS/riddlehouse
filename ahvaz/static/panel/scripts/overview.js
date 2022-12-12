
var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        order_add_pupop: false,
        order_add_loading: false,
        date: null,
        time: null,
        room: {
            id: null,
            name: null
        }
    },


    methods: {

        set_reserve_detail: function(id, name, date, hour) {
            this.date = date
            this.time = hour
            this.room = {
                id,
                name
            }
            this.order_add_pupop = true
        }
    },

    computed: {

    }
});
