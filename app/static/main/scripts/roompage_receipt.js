
var app = new Vue({
    el: '#application',

    delimiters: ["[[", "]]"],
    data: {
        current_room: null,
        step: 5,
        page_loading: true,
    },


    async mounted() {
        this.current_room = parseInt(this.$el.getAttribute("roomId"))
        AOS.init({
            offset: 20,
        });
        setTimeout(() => {
            this.page_loading = false
        }, 1000);

    },

    methods: {

        change_step: function (step) {
            if (step < this.step && this.step != 5) {
                this.step = step
            }
        },

    },
})


