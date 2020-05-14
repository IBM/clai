$(document).ready(function () {
    $('.logout').click(function() {
        $.get(`logout`, function(data) {
            if (data.status == 'LOGOUT_SUCCESS') {
                window.location.replace(`login`);
            }
        });
    })
})