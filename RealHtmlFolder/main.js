//changing nav style while scrolling

window.addEventListener('scroll',() =>{
    document.querySelector('nav').classList.toggle('window-scrolled', window.scrollY>0);
})




var swiper = new Swiper(".mySwiper", {
    pagination: {
      el: ".swiper-pagination",
      type: "progressbar",
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });