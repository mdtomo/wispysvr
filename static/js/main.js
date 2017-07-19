$(document).ready(function() {
    $('#logout').click(function() {
        window.localStorage.removeItem('token');
        window.location.href = '/'
    });
});