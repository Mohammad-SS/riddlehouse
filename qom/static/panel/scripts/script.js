
Array.prototype.remove = function () {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};

    
feather.replace()

function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

function pagination(params) {
    let pagination_items = document.getElementsByClassName('mb-pagination-item')
    Array.from(pagination_items).map(pagination_item => {
        pagination_item.addEventListener('click', (e) => {
            let page_number = pagination_item.getAttribute('g-page-number')
            if (page_number) {
                let url = new URL(window.location)
                let current_page = url.searchParams.get('page')
                url.searchParams.set('page', page_number)

                window.location = url
            }
        })
    })
}

function collapse() {

    let collapsible_list = document.querySelectorAll('[collapse-id-data]')
 
    collapsible_list.forEach(item => {

        // auto close other items
        let auto_close = item.getAttribute('collapse-auto-close')
        let auto = false
        if (auto_close === 'true') {auto = true}
        
        // bottom space
        let bottom_space = item.getAttribute('collapse-bottom-space')

        item.addEventListener('click' , function() {
            let collapsible_content_id = item.getAttribute('collapse-id-data')
            let collapsible_content = document.querySelector(`[collapse-id="${collapsible_content_id}"]`)
            if (collapsible_content.style.maxHeight) {
                collapsible_content.style.maxHeight = null;
            } else {
                if (auto) {
                    collapsible_list.forEach(i => {
                        let collapsible_content_id = i.getAttribute('collapse-id-data')
                        let collapsible_content = document.querySelector(`[collapse-id="${collapsible_content_id}"]`)
                        if (collapsible_content.style.maxHeight) {
                            collapsible_content.style.maxHeight = null;
                        }
                    })
                }
                let child_height = collapsible_content.firstElementChild.getBoundingClientRect().height

                if (bottom_space && Number.isInteger(parseInt(bottom_space))) {
                    child_height = child_height + parseInt(bottom_space)
                }
                
                collapsible_content.style.maxHeight = child_height + "px";
            }
        })
    })
}


function autocomplete() {
    let all_autocompletes = document.getElementsByClassName('gautocomplete')
    Array.from(all_autocompletes).map(async autocomplete => {
        let autocomplete_input = autocomplete.querySelector("input")
        let autocomplete_list = autocomplete.querySelector('ul.gautocomplete-list')
        await Promise.all(Array.from(autocomplete_list.childNodes).filter(item => item.nodeName == "LI").map(i => {

            let value = i.getAttribute('g-data')
            i.addEventListener("click", () => {
                autocomplete_input.classList.add("active")
                autocomplete_input.value = value
            })

        }))

        autocomplete_input.addEventListener("focus", () => {
            autocomplete_list.classList.add('active')
        })

        autocomplete_input.addEventListener("blur", () => {
            autocomplete_list.classList.remove('active')
        })

    })
}

function scroll_up() {
    var nav = document.querySelector(".gnav-container");
    var scroll_up_element = nav.querySelector('#scroll-top')
    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () { scrollFunction() };

    function scrollFunction() {
        if (document.body.scrollTop > 14 || document.documentElement.scrollTop > 14) {
            nav.classList.add('gnav-container-sticky')
            scroll_up_element.classList.add('visible')
            nav.setAttribute('onclick', 'topFunction()')
        } else {
            nav.removeAttribute('onclick')
            nav.classList.remove('gnav-container-sticky')
            scroll_up_element.classList.remove('visible')
        }

        // mybutton.style.top = `calc(100vh - 5em + ${document.documentElement.scrollTop}px)`

    }

    // When the user clicks on the button, scroll to the top of the document

}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

// scroll_up()
pagination()
collapse()
// autocomplete()

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})