
var app = new Vue({
    el: '#application',

    delimiters: ["[[", "]]"],
    data: {
        current_room: null,
        step: 1,
        accept_ruls: false,
        page_loading: true,
        reserve_date: null,
        selected_date: null,
        datepicker: false,
        changing_calendar: false,
        picked: null,
        reservable_time_list: [],
        calendar: null,
        default_calendar: null,
        current_date: get_today_jalali(),
        free_turns: '-',
        reserved_turns: '-',
        selected_turn: {
            time: null,
            price: null,
        },
        package: {
            id: null,
            price: null
        },

        player_numbers: {
            min: 1,
            max: 1,
            current: 1
        }

    },


    watch: {
        accept_ruls(newvalue, oldvalue) {
            if (newvalue === "true") {
                this.accept_ruls = true
            } else {
                this.value = false
            }
        },

        step(newvalue, oldvalue) {
            let rect = this.$refs.stepper.getBoundingClientRect()
            let scroll_pos = rect.top + window.pageYOffset - 28;
            window.scrollTo(1000, scroll_pos)
        },

        datepicker(newvalue, oldvalue) {
            if (!newvalue) {
                setTimeout(() => {
                    this.calendar = this.default_calendar
                    this.current_date = get_today_jalali()
                    create_reserve_calendar(this.calendar)
                }, 200)
            }
        }
    },

    async mounted() {
        this.current_room = parseInt(this.$el.getAttribute("roomId"))
        player_numbers_input = this.$refs.players
        this.init_player_numbers(player_numbers_input)

        AOS.init({
            offset: 20,
        });

        let calendar_data = await this.get_calendar(this.current_room, this.current_date[0], this.current_date[1])
        this.default_calendar = calendar_data
        this.calendar = calendar_data
        create_reserve_calendar(this.calendar)

        setTimeout(() => {
            this.page_loading = false
        }, 1000);

    },

    methods: {

        change_step: function (step) {
            if (step < this.step) {
                this.step = step
            }
        },

        set_reserve_date: function (date) {
            this.reserve_date = date
            this.datepicker = false
        },

        select_time: function (item, price) {
            console.log(item);
            this.selected_turn.time = item.time
            this.selected_turn.price = price
            document.querySelectorAll('.selected-time').forEach(el => el.classList.remove('selected-time'))
            document.getElementById(item.rand_id).classList.add('selected-time')
        },

        select_package(_package, price) {
            this.package = {
                id: _package,
                price: price
            }
            document.querySelectorAll('.selected-time').forEach(el => el.classList.remove('selected-time'))
            document.getElementById(`package_${_package}`).classList.add('selected-time')
        },

        get_calendar: async function (room, year, month) {
            try {
                let url = new URL(window.location).origin + `/api/calendar`
                let response = await axios.post(url, {
                    room,
                    year,
                    month
                })

                return response.data

            } catch (error) {
                console.log(error);
                return false
            }
        },

        get_next_month: async function () {
            this.changing_calendar = true
            this.current_date[1] += 1

            if (this.current_date[1] > 12) {
                this.current_date[0] += 1
                this.current_date[1] = 1
            }

            let calendar_data = await this.get_calendar(this.current_room, this.current_date[0], this.current_date[1])

            if (calendar_data) {
                this.calendar = calendar_data
                create_reserve_calendar(this.calendar)
            } else {
                this.current_date[1] -= 1
                if (this.current_date[1] < 1) {
                    this.current_date[0] -= 1
                    this.current_date[1] = 12
                }
            }

            this.changing_calendar = false
        },

        get_previous_month: async function () {
            this.changing_calendar = true
            this.current_date[1] -= 1

            if (this.current_date[1] < 1) {
                this.current_date[0] -= 1
                this.current_date[1] = 12
            }

            let calendar_data = await this.get_calendar(this.current_room, this.current_date[0], this.current_date[1])

            if (calendar_data) {
                this.calendar = calendar_data
                create_reserve_calendar(this.calendar)
            } else {
                this.current_date[1] += 1
                if (this.current_date[1] > 12) {
                    this.current_date[0] += 1
                    this.current_date[1] = 1
                }
            }

            this.changing_calendar = false
        },


        get_current_date: function () {
            return `${month_labels[this.current_date[1] - 1]} ${this.current_date[0]}`
        },

        previous_month_number: function () {
            return `${month_labels[this.current_date[1] - 2]}`
        },

        next_month_number: function () {
            return `${month_labels[this.current_date[1]]}`
        },


        select_reserve_day: function (detail, selected_date, remaining_count, reserved_count) {
            this.datepicker = false
            this.reservable_time_list = []
            this.reserve_date = selected_date
            this.selected_date = detail.date
            this.free_turns = remaining_count
            this.reserved_turns = reserved_count
            Object.entries(detail.times).forEach(item => {
                const [time, detail] = item
                if (detail.status == 'FREE') {
                    obj = { time, ...detail }
                    this.reservable_time_list.push(obj)
                }
            })
        },

        init_player_numbers: function (player_numbers_input) {
            this.player_numbers.min = parseInt(player_numbers_input.min)
            this.player_numbers.max = parseInt(player_numbers_input.max)
            this.player_numbers.current = this.player_numbers.min
            player_numbers_input.value = this.player_numbers.min
        },


        handle_players: function (e) {

            value = e.target.valueAsNumber

            if (value < this.player_numbers.min) {
                value = this.player_numbers.min
            }

            if (value > this.player_numbers.max) {
                value = this.player_numbers.max
            }

            this.player_numbers.current = value
        }

    },



    computed: {
        is_reservable_time_list_empty() {
            return this.reservable_time_list.length < 1 ? true : false
        },

        price() {
            if (this.package.id) {
                return { str: separate(this.package.price), num: this.package.price }
            }

            return { str: separate(this.selected_turn.price), num: this.selected_turn.price }
        },

        total_price() {
            if (this.package.id) {
                return { str: separate(this.player_numbers.current * this.package.price), num: this.player_numbers.current * this.package.price }
            }

            return { str: separate(this.player_numbers.current * this.selected_turn.price), num: this.player_numbers.current * this.selected_turn.price }
        }
    }
})


