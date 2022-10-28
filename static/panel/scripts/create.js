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
        packages: []
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

        reset_time_picker: function(e) {
            this.$refs.timepicker.value = '0'
        },

        add_package: function(e) {

            let value = this.$refs.add_package.value.trim()

            if (!value || value == '' || this.packages.filter(package => package.price == value).length != 0) {
                return
            }

            let package_length = this.packages.length
            this.packages.push({
                id : (package_length + 1),
                name: `پکیج شماره ` + (package_length + 1),
                price: value
            })

            this.$refs.add_package.value = null
            
        },

        removePackage: function(id) {
            this.packages = this.packages.filter(package => package.id != id)
        }
        // handle_room_mode: function(e) {
        //     console.log(e.target.value);
        // }
    },
});
