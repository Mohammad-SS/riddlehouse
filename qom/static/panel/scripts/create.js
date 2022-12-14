var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        tags: [],
        tag_remove_all: false,
        time: '00:00',
        room_mode: 'real',
        packages: [],
        banner: false

    },

    mounted: function () {
        if (document.room_obj) {
            console.log(document.room_obj)
            // set weekdays
            let weekdays = document.room_obj.weekdays
            if (weekdays && weekdays.length > 0) {
                weekdays.map(wd => document.getElementById(`d-${wd}`).checked = true)
            }

            // set default room hours
            let default_hours = document.room_obj.default_hours
            if (default_hours && default_hours.length > 0) {
                this.tags = default_hours
            } else {
                this.tags = []
            }

            // set room type
            let room_type = document.room_obj.room_type
            if (room_type) {
                console.log("HERE");
                this.room_mode = room_type == "REAL" ? 'real' : 'box'
            }

            // set room pakcages
            let packages = document.room_obj.box_packages
            if (packages && packages.length > 0) {
                packages.map((package, index) => {
                    this.packages.push({
                        id: (index + 1),
                        name: `پکیج شماره ` + (index + 1),
                        price: package
                    })
                })
            }
        }
    },

    watch: {
        room_mode(new_value, old_value) {
            if (new_value != 'box') {
                this.packages = []
                this.tags = []
            } else {
                this.tags = ["12:00"]
            }
        }
    },

    methods: {
        addTag() {
            if (this.room_mode != 'box') {
                if (this.time.trim().length === 0 || this.tags.includes(this.time.trim())) {
                    return
                }
                this.tags.push(this.time.trim())
            }
        },
        removeTag(tag) {
            if (this.room_mode != 'box') {
                this.tags = this.tags.filter(t => t !== tag)
            }
        },

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

        reset_time_picker: function (e) {
            this.$refs.timepicker.value = '0'
        },

        add_package: function (e) {

            let value = this.$refs.add_package.value.trim()

            if (!value || value == '' || this.packages.filter(package => package.price == value).length != 0) {
                return
            }

            let package_length = this.packages.length
            this.packages.push({
                id: (package_length + 1),
                name: `پکیج شماره ` + (package_length + 1),
                price: value
            })

            this.$refs.add_package.value = null

        },

        removePackage: function (id) {
            this.packages = this.packages.filter(package => package.id != id)
        },

        handle_banner: async function (e) {
            // if (this.banner) {
            //     this.banner = false
            //     await new Promise((resolve, reject) => setTimeout(() => {
            //         resolve(true)
            //     }, 300))
            // }
            this.banner = e.target.files[0]
            this.banner.src = URL.createObjectURL(this.banner)
        },

        formatBytes: function (bytes, decimals = 2) {
            if (!+bytes) return '0 Bytes'

            const k = 1024
            const dm = decimals < 0 ? 0 : decimals
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

            const i = Math.floor(Math.log(bytes) / Math.log(k))

            return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
        },

        reset_form: function (e) {
            this.banner = false
            this.$refs.room_create_form.reset()
        },

        handle_tag_remove_all: function () {
            if (this.tag_remove_all) {
                this.tags = []
                this.tag_remove_all = false
            } else {
                if (this.tags.length > 0) {
                    this.tag_remove_all = true
                }
            }
        },



        replace_room_data: function (e) {
            console.log("HERE replace_room_data");
        }, 

        handle_create_submit: function(e) {
             e.preventDefault();
            let form = this.$refs.room_create_form
            if (form.checkValidity()) {
                e.target.disabled = true;
                form.submit()
            }
        },

        handle_edit_submit: function(e) {
             e.preventDefault();
            let form = this.$refs.room_edit_form
            if (form.checkValidity()) {
                e.target.disabled = true;
                form.submit()
            }
        }


    },

    computed: {

        get_banner_name() {
            if (this.banner) {
                let name = this.banner.name.split('.')
                name.pop()
                name = name.join()
                if (name.length > 20) {
                    name = name.substr(0, 20) + "..."
                }
                return name
            }

            return false
        },

        get_banner_type() {
            if (this.banner) {
                return this.banner.type
            }

            return false
        },

        get_banner_size() {
            if (this.banner) {
                return this.formatBytes(this.banner.size)
            }
            return false
        },

        get_banner_src() {
            if (this.banner) {
                return this.banner.src
            }
            return false
        }
    }
});
