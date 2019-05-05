var appState = undefined

var registerAppState = state => appState = state

var onSignIn = () => {
    let username = $("#username").val()
    let password = $("#password").val()

    let credentials = { username, password }
    
    $.ajax({
        type: 'POST',
        url: `/signin?state=${appState}`,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(credentials),
        success: () => window.location.href = "/category/",
        error: () => $('#login_error').html(`
            <div id="login_error" class="alert alert-danger alert-dismissible fade show" role="alert">
                <strong>Login Error!</strong> Please, try again!
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>`)
    });
}

var cancelSignIn = () => {
    window.location.href = "/category/"
}

var onLoad = () => {
    gapi.load('auth2', () => {
        auth2 = gapi.auth2.init()
        btn_gplus_sign_in = document.getElementById('googleSignIn');
        auth2.attachClickHandler(btn_gplus_sign_in, {}, onGSignIn)
    })
}

var onGSignIn = googleUser => {
    let id_token = googleUser.getAuthResponse().id_token
    if (id_token) {
        $.ajax({
            type: 'POST',
            url: `/gconnect?state=${appState}`,
            processData: false,
            data: id_token,
            contentType: 'application/octet-stream; charset=utf-8',
            success: function(result) {
                if (result) {
                    window.location.href = "/category/"
                } else {
                    $('#login_error').removeAttr('hidden')
                }
            }
        });
    } else {
        $('#login_error').removeAttr('hidden')
    }
}

var signOut = () => {
    let auth2 = gapi.auth2.getAuthInstance()
    auth2.signOut().then(function () {
        $.ajax({
            type: 'POST',
            url: '/logout',
            processData: false,
            contentType: 'application/octet-stream; charset=utf-8',
            success: () => window.location.href = "/category/"
        });
    });
}