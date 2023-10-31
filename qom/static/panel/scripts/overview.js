var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        order_add_pupop: false,
        vip_pupop: false,
        order_add_loading: false,
        vip_loading: false,
        date: null,
        time: null,
        room: {
            id: null,
            name: null
        },
        vip: {
            is_vip: null,
            price_per_unit: null,
            pre_pay: null
        }
    },


    methods: {

        set_reserve_detail: function (id, name, date, hour) {
            this.date = date
            this.time = hour
            this.room = {
                id,
                name
            }
            this.order_add_pupop = true
        },

        set_vip_detail: function (id, name, date, hour, is_vip, unit_price, pre_pay) {
            this.date = date
            this.time = hour
            this.room = {
                id,
                name
            },
            this.vip ={
                is_vip: is_vip,
                price_per_unit: unit_price,
                pre_pay: pre_pay
            }
            this.vip_pupop = true
        },

        handle_order_submit: function (e) {
            e.preventDefault();
            let form = this.$refs.order_add_form
            if (form.checkValidity()) {
                this.order_add_loading = true
                form.submit()
            } else {
                this.order_add_loading = false
            }

        },

        handle_vip_submit: function (e, action) {
            e.preventDefault();
            let form = this.$refs.vip_form
            if (form.checkValidity()) {
                this.vip_loading = true
                form.submit()
            } else {
                this.vip_loading = false
            }

        }
    },

    computed: {}
});
