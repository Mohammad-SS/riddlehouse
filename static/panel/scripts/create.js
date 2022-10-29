// Vue.component('tags-input', {
//     template: `
//       <div class="tags-input">

//         <label id='timelabel' for="time"></label>

//       </div>
//     `,
//     props: ['value'],
//     data() {
//         return {
//             newTag: '',
//         }
//     },
// methods: {
//     addTag() {
//         if (this.newTag.trim().length === 0 || this.value.includes(this.newTag.trim())) {
//             return
//         }
//         this.$emit('input', [...this.value, this.newTag.trim()])
//         this.newTag = ''
//     },
//     removeTag(tag) {
//         this.$emit('input', this.value.filter(t => t !== tag))
//     },
// },
// })

var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        tags: [],
        time: '00:00',
        room_mode: 'real',
        packages: [],
        banner: false

    },

    methods: {
        addTag() {
            if (this.time.trim().length === 0 || this.tags.includes(this.time.trim())) {
                return
            }
            this.tags.push(this.time.trim())
        },
        removeTag(tag) {
            this.tags = this.tags.filter(t => t !== tag)
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

        reset_form: function(e) {
            this.banner = false
            this.$refs.room_create_form.reset()
        }

    },

    computed: {

        get_banner_name() {
            if (this.banner) {
                let name = this.banner.name.split('.')
                name.pop()
                name = name.join()
                if (name.length > 20) {
                    name = name.substr(0,20) + "..."
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


// lastModified
// :
// 1664467588000
// lastModifiedDate
// :
// Thu Sep 29 2022 19:36:28 GMT+0330 (Iran Standard Time) {}
// name
// :
// "ALKATRAZ2.jpg"
// size
// :
// 14285
// type
// :
// "image/jpeg"
// webkitRelativePath
// :
// ""