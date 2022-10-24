
var app = new Vue({
    el: '#application',

    delimiters: ["[[", "]]"],
    data: {
        current_room: null,
        step: 1,
        accept_rols: false,
        page_loading: true,
        reserve_date: null,
        datepicker: false,
        changing_calendar: false,
        picked: null,
        reservable_time_list: [],
        calendar: null,
        default_calendar: null,
        current_date: get_today_jalali(),
        free_turns: '-',
        reserved_turns: '-',
        selected_turn: null

    },


    watch: {
        step(newvalue, oldvalue) {
            let rect = this.$refs.stepper.getBoundingClientRect()
            let scroll_pos = rect.top + window.pageYOffset - 28;
            window.scrollTo(1000, scroll_pos)
        },

        datepicker(newvalue, oldvalue) {
            console.log(oldvalue, newvalue);
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

        select_time: function (item) {
            this.selected_turn = item.time
            document.querySelectorAll('.selected-time').forEach(el => el.classList.remove('selected-time'))
            document.getElementById(item.rand_id).classList.add('selected-time')
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
            this.free_turns = remaining_count
            this.reserved_turns = reserved_count
            Object.entries(detail.times).forEach(item => {
                const [time, detail] = item
                if (detail.status == 'FREE') {
                    obj = { time, ...detail }
                    this.reservable_time_list.push(obj)
                }
            })
        }
    },

    computed: {
        is_reservable_time_list_empty() {
            return this.reservable_time_list.length < 1 ? true : false
        }
    }
})


