var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        add_schedule_pupop: false,
        add_loschedule_ading: false,
        tags: [],
        tag_remove_all: false,
        time: '00:00',
        schedule_mode: 1,

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

        addTag() {
            if (this.time.trim().length === 0 || this.tags.includes(this.time.trim())) {
                return
            }
            this.tags.push(this.time.trim())
        },
        removeTag(tag) {
            this.tags = this.tags.filter(t => t !== tag)
        },

        
        reset_time_picker: function (e) {
            this.$refs.timepicker.value = '0'
        },

        handle_tag_remove_all: function() {
            if (this.tag_remove_all) {
                this.tags = []
                this.tag_remove_all = false
            } else {
                if (this.tags.length > 0) {
                    this.tag_remove_all = true
                }
            }
        }
    },
});


jalaliDatepicker.startWatch();

