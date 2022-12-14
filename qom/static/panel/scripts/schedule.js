var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        remove_schedule_pupop: false,
        remove_schedule_loading: false,
        remove_url: null
    },

    methods: {
    
        handle_schedule_remove_submit: function(e) {
            e.preventDefault();
            let form = this.$refs.schedule_remove_form
            if (form.checkValidity()) {
                this.remove_schedule_loading = true;
                form.submit()
            } else {
                this.remove_schedule_loading = false;
            }
            
        },

        handle_remove_schedule: function(url) {
            this.remove_url = url
            this.remove_schedule_pupop = true
        }
    },
});

