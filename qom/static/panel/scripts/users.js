let modal = mdb.Modal.getOrCreateInstance('#userAddModal')
let userDeleteModal = document.getElementById("userDeleteModal")
let userChangePasswordModal = document.getElementById("userChangePasswordModal")


if (userDeleteModal) {
    userDeleteModal.addEventListener('show.mdb.modal', event => {

        
        // Button that triggered the modal
        let button = event.relatedTarget
        // Extract info from data-bs-* attributes
        let user_pk = button.getAttribute('data-mdb-pk')
        let user_name = button.getAttribute('data-mdb-username')
        let user_fullname = button.getAttribute('data-mdb-fullname')
        // If necessary, you could initiate an Ajax request here
        // and then do the updating in a callback.

        // Update the modal's content.
        let pkInput = userDeleteModal.querySelector('input[name="pk"]')
        let usernameEl = userDeleteModal.querySelector('span.user-username')
        let fullnameEl = userDeleteModal.querySelector('span.user-fullname')

        console.log(usernameEl, user_name);
        

        pkInput.value = user_pk
        usernameEl.innerHTML = user_name
        fullnameEl.innerHTML = user_fullname

    })
}
if (userChangePasswordModal) {
    userChangePasswordModal.addEventListener('show.mdb.modal', event => {

        
        // Button that triggered the modal
        let button = event.relatedTarget
        // Extract info from data-bs-* attributes
        let user_pk = button.getAttribute('data-mdb-pk')

        // If necessary, you could initiate an Ajax request here
        // and then do the updating in a callback.

        // Update the modal's content.
        let pkInput = userChangePasswordModal.querySelector('input[name="pk"]')

        pkInput.value = user_pk


    })
}