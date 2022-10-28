var app = new Vue({
    el: '#app',

    delimiters: ["[[", "]]"],
    data: {
        filter_tab: 1,
        account: null,
        min_date: null,
        max_date: null,

        room_add_dialog: false

    },

    watch: {
        // whenever question changes, this function will run
        filter_tab: async function (newTab, oldTab) {

            await new Promise((resolve, reject)=> {
                setTimeout(() => {
                    
                }, 50);

                resolve(true)
            })

            let order_items = document.querySelectorAll('tbody.gorder-list-tbody tr.gorder-item')
            console.log(order_items.length);
            if (order_items.length < 1) {
                document.querySelector('tr.not-available').classList.remove('d-none')
            } else {
                document.querySelector('tr.not-available').classList.add('d-none')
            } 
        }
    },
    
    mounted: function (e) {

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        this.min_date = urlParams.get('min_date')
        this.max_date = urlParams.get('max_date')

        const account = urlParams.get('account')
        if (account == 'all') {
            this.account = null
        } else {
            this.account = account
        }


    },

    methods: {
        handle_filters: function (e) {

            let new_location = new URL(location.protocol + '//' + location.host + location.pathname)
            let filter_params = {}
            if (this.account) {
                if (this.account != 'all') {
                    filter_params.account = this.account
                }
            }

            if (this.min_date) {
                filter_params.min_date = this.min_date
            }

            if (this.max_date) {
                filter_params.max_date = this.max_date
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
            
            let includes_params = ["account", "min_date", "max_date"].filter(item => params_keys.includes(item))

            if (!Boolean(includes_params.length)) {
                this.min_date = null
                this.max_date = null
                this.account = null
            } else {    
                window.location = location.protocol + '//' + location.host + location.pathname
            }
        }
    },

    computed: {
        // a computed getter
        clear_filter_btn() {
            // `this` points to the component instance
            return (this.account == null) && this.min_date == null && this.max_date == null ? true : false
        }
    }

})
