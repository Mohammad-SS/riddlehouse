// swiper
var swiper = new Swiper(".head-slider", {
  // effect: "fade",
  pagination: {
    el: ".swiper-pagination",
    dynamicBullets: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  grabCursor: true,
  centeredSlides: true,
  loop: true,
});


var cube_tip_swiper = new Swiper(".cube-tip-box", {
  effect: "cube",
  grabCursor: true,
  cubeEffect: false,
  loop: true,
  autoplay: {
    delay: 4000,
  },

});


var coverflow_tip_swiper = new Swiper(".coverflow-tip-box", {
  effect: "coverflow",
  grabCursor: true,
  centeredSlides: true,
  slidesPerView: "auto",
  coverflowEffect: {
    rotate: 50,
    stretch: 0,
    depth: 100,
    modifier: 1,
    slideShadows: true,
  },
  loop: true,
  autoplay: {
    delay: 4000,
  },
});

