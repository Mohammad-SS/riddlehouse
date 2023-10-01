function create_reserve_calendar(date) {

    // get date object
    let now = new Date()

    // calendar selector
    let calendar_element = document.querySelector('.calendar')
    calendar_element.innerHTML = ''
    // weekday labels
    let weekday_labels = ["ش", "ی", "د", "س", "چ", "پ", "ج"]
    let weekday_labels_full = [
        "شنبه",
        "یکشنبه",
        "دوشنبه",
        "سه شنبه",
        "چهارشنبه",
        "پنجشنبه",
        "جمعه",
    ]
    let month_labels = [
        'فروردین',
        'اردیبهشت',
        'خرداد',
        'تیر',
        'مرداد',
        'شهریور',
        'مهر',
        'آبان',
        'آذر',
        'دی',
        'بهمن',
        'اسفند',
    ]

    // convert today to jalali
    let today_day = now.getDate()
    let today_month = now.getMonth() + 1
    let today_year = now.getFullYear()
    const [j_y, j_m, j_d] = convert_to_jalali(today_year, today_month, today_day)

    // // generate calendar header
    // let calendar_header = calendar_element.previousElementSibling
    // calendar_header.querySelector('.today').innerHTML = `${month_labels[j_m - 1]} ${j_y}`

    // assign weekday labels to calendar
    let week_days = document.createElement('ul')
    weekday_labels.forEach(week_day => {
        let week_day_item = document.createElement('li')
        week_day_item.classList.add('weekday')
        week_day_item.innerHTML = week_day
        week_days.appendChild(week_day_item)
    })
    calendar_element.appendChild(week_days)

    // assign days to calendar
    Object.entries(date).forEach(week => {
        let week_row = document.createElement('ul')
        const [week_number, week_days] = week;

        // handle empty weekdays
        if (week_number == 0) {
            empty_week_day = {}
            let length = Object.keys(week_days).length
            let count = 7 - length
            for (let index = 0; index < count; index++) {
                Object.assign(empty_week_day, { [index + 1]: "test" })
                let week_day_item = document.createElement('li')
                week_day_item.classList.add('empty')
                // append week row to calendar
                week_row.appendChild(week_day_item)
            }
        }

        // add days to calendar
        Object.entries(week_days).forEach(week_day => {
            const [day_number, day_detail] = week_day
            let week_day_item = document.createElement('li')
            let day_remaining_turn_el = document.createElement('span')

            // Specify selectable items (Today until next week - 7 days)
            if (day_detail.selectable) {
                week_day_item.classList.add('selectable-day')
                week_day_item.innerText = day_number
                let remaining_count = Object.values(day_detail.times).filter(item => item.status == 'FREE').length
                let reserved_count = Object.values(day_detail.times).filter(item => item.status == 'RESERVED').length
                    if (remaining_count == 0) {
                    week_day_item.classList.add('full')
                }
                day_remaining_turn_el.innerText = remaining_count
                week_day_item.appendChild(day_remaining_turn_el)

                let selected_date = `${weekday_labels_full[day_detail.weekday - 1]} - ${day_detail.date}`
                week_day_item.addEventListener('click', () => {
                    app.select_reserve_day(day_detail, selected_date, remaining_count, reserved_count)
                })

            } else {
                week_day_item.innerText = day_number
            }

            // append week row to calendar
            week_row.appendChild(week_day_item)
        })

        // append week row to calendar
        calendar_element.appendChild(week_row)
    })
}
