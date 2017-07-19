// Wispysvr Login handler
$(document).ready(function() {
    console.log('ready');
    if (window.localStorage.token) {
        window.localStorage.removeItem('token');
        updateStatus('Logged out successfully.', 'success');
    }
    $('button').click(function() {
        console.log('clicked');
        const credentials = { 'username': $('#username').val(), 'password': $('#password').val() }
        $.post('/login', credentials)
              .done(function(data, status, xhr) {
                  window.localStorage.setItem('token', data[0].access_token);
                  $.ajaxSetup({ 
                      headers:{ "Authorization": "Bearer " + window.localStorage.token }
                  });
                  console.log('Data ' + data[0].access_token + status + xhr);
                  updateStatus('Logging in...', 'success');
                  $.get(data[1].redirect, function(data, status) {
                      console.log("GET Data " + data + "Status " + status);
                      if (status == 'success') {
                          $("#mainView").replaceWith(data);
                      } else {
                          updateStatus('Could not start live view.', 'danger');
                      }
                  });      
              })
              .fail(function(xhr, status, error) {
                  console.log('Fail ' + xhr.responseText + status + error);
                  updateStatus(xhr.responseText, 'danger');
              });
        });

    function updateStatus(statusMsg, alertType) {
        $('#status').html('<div class="alert alert-' + alertType + '">' + statusMsg + '</div>');
    };

});


// $(document).ready(function() {
//         console.log("ready");
//         if (window.localStorage.token) {
//             window.localStorage.removeItem('token');
//         }
//         $("button").click(function() {
//             console.log("clicked");
//             const credentials = { "username": $("#username").val(), "password": $("#password").val() }
//             $.post("/login", credentials, function(data, status) {
//                     console.log("Data: " + data[0].access_token + " Redirect " + data[1].redirect + "\nStatus: " + status);
//                     window.localStorage.setItem('token', data[0].access_token);
//                     $.ajaxSetup({ 
//                         headers:{ "Authorization": "Bearer " + window.localStorage.token }
//                     });
//                     if (data[1].redirect) {
//                       $.get(data[1].redirect, function(data, status) {
//                           console.log("GET Data " + data + "Status " + status);
//                           if (status == 'success') {
//                               $("#mainView").replaceWith(data);
//                               console.log("replaced");
//                           } else {
//                               $("#mainView").replaceWith("<div> Could not start live view. </div>");
//                           }
//                       });
//                     } else {
//                         console.log("Incorrect credentials.");
//                         $("#status").html("<div class='alert alert-warning'>Incorrect username or password.</div>");
//                     }
                    
//             });
//         });
// });