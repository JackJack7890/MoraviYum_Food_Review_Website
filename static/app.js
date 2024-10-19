var submit_button = document.getElementById("submit_button")

function submit() {
    var user_handle = document.getElementById("username_input").value
    if (user_handle === "") {
        alert("Please enter a username")
        return;
    }
    fetch('/store_user_handle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_handle: user_handle
        }),
    })
    var path = window.location
    var endpoint = "reviw"
    return `${path}.origin/${endpoint}`
}

submit_button.addEventListener('click', () => {
    submit()
    const BASE_URL = window.location.origin
    window.location.href = BASE_URL + '/review';
})

