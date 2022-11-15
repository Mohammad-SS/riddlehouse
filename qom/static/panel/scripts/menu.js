


const mediaQueryList = window.matchMedia('(max-width: 1024px)');
let menu = document.querySelector('.mb-menu')
let content = document.querySelector('.mb-content')
let nav = document.querySelector('.mb-nav-container')
let hamb = document.querySelector('input#hamb-menu')


hamb_action = () => {
    if (hamb.checked) {
        menu.classList.add('mb-menu-collapse')
        content.classList.add('mb-collapse')
    } else {
        menu.classList.remove('mb-menu-collapse')
        content.classList.remove('mb-collapse')
    }
}

hamb_handle = (init) => {
    hamb.checked = false
    hamb_action()
    if (mediaQueryList.matches) {
        hamb.addEventListener('change', hamb_action)
    } else {
        hamb.removeEventListener('change', hamb_action)
    }
}


hamb_handle(true)
mediaQueryList.addEventListener('change', () => hamb_handle(false))
