var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        order_add_pupop: false,
        order_add_loading: false,
        selected_rooms: [],
        time: '00:00',
        room: null,
        min_date: null,
        max_date: null,
        filter_mode: null
    },

    
    mounted: function (e) {

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        this.min_date = urlParams.get('min_date')
        this.max_date = urlParams.get('max_date')
        this.filter_mode = urlParams.get('filter_mode')

        const room = urlParams.get('room')
        if (room == 'all') {
            this.room = null
        } else {
            this.room = room
        }


    },


    methods: {
        two_digits: (num) => num.toLocaleString('en-US', {
            minimumIntegerDigits: 2,
            useGrouping: false
        }),

        set_time: function (e) {
            let hour = ''
            let min = ''
            let value = e.target.value
            hour = parseInt(value / 12)
            min = parseInt((value * 5) - (hour * 60))
            this.time = this.two_digits(hour) + ":" + this.two_digits(min)
        },

        handle_filters: function (e) {

            let new_location = new URL(location.protocol + '//' + location.host + location.pathname)
            let filter_params = {}
            if (this.room) {
                if (this.room != 'all') {
                    filter_params.room = this.room
                }
            }

            if (this.min_date) {
                filter_params.min_date = this.min_date
            }

            if (this.max_date) {
                filter_params.max_date = this.max_date
            }

            if (this.filter_mode) {
                filter_params.filter_mode = this.filter_mode
            }

            for ([key, value] of Object.entries(filter_params)) {
                new_location.searchParams.append(key, value)
            }


            if (!this.clear_filter_btn) {
                window.location = new_location.href
            }

        },

        clear_filters: function (e) {
            const params = new URLSearchParams(window.location.search)
            const params_keys = Array.from(params).map(param => param[0])
            
            let includes_params = ["room", "min_date", "max_date", 'filter_mode'].filter(item => params_keys.includes(item))

            if (!Boolean(includes_params.length)) {
                this.min_date = null
                this.max_date = null
                this.room = null
                this.filter_mode = null
            } else {    
                window.location = location.protocol + '//' + location.host + location.pathname
            }
        }
    },

    computed: {
        // a computed getter
        clear_filter_btn() {
            // `this` points to the component instance
            return (this.room == null) && this.min_date == null && this.max_date == null && this.filter_mode == null ? true : false
        }
    }
});

jalaliDatepicker.startWatch();