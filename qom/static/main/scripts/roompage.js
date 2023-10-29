var app = new Vue({
  el: "#application",

  delimiters: ["[[", "]]"],
  data: {
    submit_loading: false,
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
    today_date: document.today,
    current_date: get_today_jalali(document.today),
    free_turns: "-",
    reserved_turns: "-",
    coupan: {
      code: "",
      amount: null,
      type: null,
      valid: false,
    },

    selected_turn: {
      time: null,
      price: null,
      pre_pay: null,
      is_vip: null,
    },
    package: {
      id: null,
      price: null,
    },

    player_numbers: {
      min: 1,
      max: 1,
      current: 1,
    },
  },

  watch: {
    accept_ruls(newvalue, oldvalue) {
      if (newvalue === "true") {
        this.accept_ruls = true;
      } else {
        this.value = false;
      }
    },

    step(newvalue, oldvalue) {
      let rect = this.$refs.stepper.getBoundingClientRect();
      let scroll_pos = rect.top + window.pageYOffset - 28;
      window.scrollTo(1000, scroll_pos);
    },

    datepicker(newvalue, oldvalue) {
      if (!newvalue) {
        setTimeout(() => {
          this.calendar = this.default_calendar;
          this.current_date = get_today_jalali(this.today_date);
          create_reserve_calendar(this.calendar);
        }, 200);
      }
    },
  },

  async mounted() {
    this.current_room = parseInt(this.$el.getAttribute("roomId"));
    player_numbers_input = this.$refs.players;
    this.init_player_numbers(player_numbers_input);

    AOS.init({
      offset: 20,
    });

    let calendar_data = await this.get_calendar(
      this.current_room,
      this.current_date[0],
      this.current_date[1]
    );
    this.default_calendar = calendar_data;
    this.calendar = calendar_data;
    create_reserve_calendar(this.calendar);

    setTimeout(() => {
      this.page_loading = false;
    }, 1000);
  },

  methods: {
    change_step: function (step) {
      if (step < this.step) {
        this.step = step;
      }
    },

    set_reserve_date: function (date) {
      this.reserve_date = date;
      this.datepicker = false;
    },

    select_time: function (item, price) {
      this.selected_turn.time = item.time;
      this.selected_turn.price = price;
      this.selected_turn.pre_pay = item.pre_pay;
      this.selected_turn.is_vip = item.is_vip;
      document
        .querySelectorAll(".selected-time")
        .forEach((el) => el.classList.remove("selected-time"));
      document.getElementById(item.rand_id).classList.add("selected-time");
    },

    select_package(_package, price) {
      this.package = {
        id: _package,
        price: price,
      };
      document
        .querySelectorAll(".selected-time")
        .forEach((el) => el.classList.remove("selected-time"));
      document
        .getElementById(`package_${_package}`)
        .classList.add("selected-time");
    },

    remove_selected: function () {
      document
        .querySelectorAll(".selected-time")
        .forEach((el) => el.classList.remove("selected-time"));
    },

    get_calendar: async function (room, year, month) {
      try {
        let url = new URL(window.location).origin + `/api/calendar`;
        let response = await axios.post(url, {
          room,
          year,
          month,
        });

        return response.data;
      } catch (error) {
        console.log(error);
        return false;
      }
    },

    get_next_month: async function () {
      this.changing_calendar = true;
      this.current_date[1] += 1;

      if (this.current_date[1] > 12) {
        this.current_date[0] += 1;
        this.current_date[1] = 1;
      }

      let calendar_data = await this.get_calendar(
        this.current_room,
        this.current_date[0],
        this.current_date[1]
      );

      if (calendar_data) {
        this.calendar = calendar_data;
        create_reserve_calendar(this.calendar);
      } else {
        this.current_date[1] -= 1;
        if (this.current_date[1] < 1) {
          this.current_date[0] -= 1;
          this.current_date[1] = 12;
        }
      }

      this.changing_calendar = false;
    },

    get_previous_month: async function () {
      this.changing_calendar = true;
      this.current_date[1] -= 1;

      if (this.current_date[1] < 1) {
        this.current_date[0] -= 1;
        this.current_date[1] = 12;
      }

      let calendar_data = await this.get_calendar(
        this.current_room,
        this.current_date[0],
        this.current_date[1]
      );

      if (calendar_data) {
        this.calendar = calendar_data;
        create_reserve_calendar(this.calendar);
      } else {
        this.current_date[1] += 1;
        if (this.current_date[1] > 12) {
          this.current_date[0] += 1;
          this.current_date[1] = 1;
        }
      }

      this.changing_calendar = false;
    },

    get_current_date: function () {
      return `${month_labels[this.current_date[1] - 1]} ${
        this.current_date[0]
      }`;
    },

    previous_month_number: function () {
      return `${month_labels[this.current_date[1] - 2]}`;
    },

    next_month_number: function () {
      return `${month_labels[this.current_date[1]]}`;
    },

    select_reserve_day: function (
      detail,
      selected_date,
      remaining_count,
      reserved_count
    ) {
      if (this.selected_date != detail.date) {
        this.selected_turn.time = null;
        this.selected_turn.price = null;
        this.selected_turn.pre_pay = null;
        this.remove_selected();
      }
      this.datepicker = false;
      this.reservable_time_list = [];
      this.reserve_date = selected_date;
      this.selected_date = detail.date;
      this.free_turns = remaining_count;
      this.reserved_turns = reserved_count;
      Object.entries(detail.times).forEach((item) => {
        const [time, detail] = item;
        if (detail.status == "FREE") {
          obj = { time, ...detail };
          this.reservable_time_list.push(obj);
        }
      });
    },

    init_player_numbers: function (player_numbers_input) {
      this.player_numbers.min = parseInt(player_numbers_input.min);
      this.player_numbers.max = parseInt(player_numbers_input.max);
      this.player_numbers.current = this.player_numbers.min;
      player_numbers_input.value = this.player_numbers.min;
    },

    handle_players: function (e) {
      value = e.target.valueAsNumber;

      if (value < this.player_numbers.min) {
        value = this.player_numbers.min;
      }

      if (value > this.player_numbers.max) {
        value = this.player_numbers.max;
      }

      this.player_numbers.current = value;
    },

    check_mobile: function (value) {
      value = value.replace(/\s+/g, "");
      value = value.replace(/\+/g, "");
      value = value.replace(/^(09|989|9)/g, "09");
      var result = value.match(/^(09)[0-9]\d{8}$/g);
      return result;
    },

    show_toast: function (text) {
      Toastify({
        text: text,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
          background: "var(--mb-original-red)",
        },
        onClick: function () {}, // Callback after click
      }).showToast();
    },

    numberToEn: function (number) {
      number = `${number}`;

      let schema = {
        "۰": 0,
        "۱": 1,
        "۲": 2,
        "۳": 3,
        "۴": 4,
        "۵": 5,
        "۶": 6,
        "۷": 7,
        "۸": 8,
        "۹": 9,
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 8,
        9: 9,
      };

      let numbers_array = Array.from(number);
      numbers_array = numbers_array.map((number) => schema[number]);
      return numbers_array.join("");
    },
    handle_information_submit: function (e, min_player, max_player) {
      e.preventDefault();
      let min = parseInt(min_player);
      let max = parseInt(max_player);
      this.submit_loading = true;
      let form = this.$refs.information_form;
      let inputs = this.$refs.information_form.querySelectorAll(
        "#phone,#name,#persons"
      );

      let name = this.$refs.information_form.querySelector("#name");
      let phone = this.$refs.information_form.querySelector("#phone");
      let persons = this.$refs.information_form.querySelector("#persons");

      if (!name.value) {
        this.show_toast("نام و نام خانودگی نمیتواند خالی باشد");
        this.submit_loading = false;
        return;
      }
      if (!phone.value) {
        this.show_toast("وارد کردن شماره موبایل الزامی است");
        this.submit_loading = false;
        return;
      }
      if (!persons.value) {
        this.show_toast("لطفا اطلاعات فرم را با دقت بیشتری تکمیل کنید");
        this.submit_loading = false;
        return;
      }

      if (parseInt(persons.value) < min) {
        console.log("here");
        this.show_toast(
          `تعداد نفرات وارد شده نمیتواند کمتر از ${min} نفر باشد`
        );
        this.submit_loading = false;
        return;
      }
      if (parseInt(persons.value) > max) {
        console.log("here1");
        this.show_toast(
          `تعداد نفرات وارد شده نمیتواند بیشتر از ${max} نفر باشد`
        );
        this.submit_loading = false;
        return;
      }

      if (!this.check_mobile(this.numberToEn(`${phone.value}`))) {
        this.show_toast("لطفا شماره موبایل را تصحیح کنید");
        this.submit_loading = false;
        phone.value = this.numberToEn(`${phone.value}`);
        return;
      }

      if (form.checkValidity()) {
        form.submit();
      } else {
        this.show_toast("لطفا اطلاعات فرم را با دقت بیشتری تکمیل کنید");
        this.submit_loading = false;
        return;
      }
    },
    check_coupan: async function () {
      try {
        let url =
          new URL(window.location).origin +
          `/api/check-coupon?room=${this.current_room}&coupon=${this.coupan.code}`;
        let response = await axios.get(url);
        if (!response.data.valid) {
          this.show_toast("کد تخفیف وارد شده معتبر نمیباشد");
        }

        let total = this.total_price.num;
        this.coupan = {
          ...this.coupan,
          amount: response.data.amount,
          type: response.data.type,
          valid: response.data.valid
        };

        return response.data;
      } catch (error) {
        return false;
      }
    },
  },

  computed: {
    is_reservable_time_list_empty() {
      return this.reservable_time_list.length < 1 ? true : false;
    },

    price() {
      if (this.package.id) {
        return { str: separate(this.package.price), num: this.package.price };
      }

      return {
        str: separate(this.selected_turn.price),
        num: this.selected_turn.price,
      };
    },

    total_price() {
      if (this.package.id) {
        return {
          str: separate(this.player_numbers.current * this.package.price),
          num: this.player_numbers.current * this.package.price,
        };
      }

      return {
        str: separate(this.player_numbers.current * this.selected_turn.price),
        num: this.player_numbers.current * this.selected_turn.price,
      };
    },

    total_price_with_off() {
      if (!this.coupan.valid) {
        return this.total_price;
      }

      let off_type = this.coupan.type;
      let off_amount = this.coupan.amount;
      let total_price =
        off_type == "percent" 
        ? this.total_price - ((this.total_price * off_amount) / 100) 
        : this.total_price - off_amount;

     return { str: separate(total_price), num: total_price }
    },
  },
});
