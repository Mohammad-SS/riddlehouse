function collapse_nav(e) {
    let nav_items = document.querySelector('.nav-items')
    if (nav_items.style.maxHeight) {
        nav_items.classList.remove('mt-3')
        nav_items.style.maxHeight = null
    } else {
        nav_items.classList.add('mt-3')
        nav_items.style.maxHeight = nav_items.scrollHeight + 'px'
    }
}

