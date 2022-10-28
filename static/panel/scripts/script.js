
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


function pagination(params) {
    let pagination_items = document.getElementsByClassName('gpagination-item')
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

    let coll = document.getElementsByClassName("gcollapsible");
    let i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function () {
            this.classList.toggle("gcollapse-active");
            let icon = this.querySelector('.gcollapsible-icon')
            icon.classList.toggle("gcollapsible-icon-rotate")
            let content = this.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    }
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
// pagination()
// collapse()
// autocomplete()