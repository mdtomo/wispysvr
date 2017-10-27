// Wispysvr login
var app = new Vue({
  el: '#app',
  data: {
    username: '',
    password: '',
    message: '',
    messageIsHidden: true,
    messageIsError: false,
    messageIsSuccess: false
  },
  methods: {
    login() {
        var data = new URLSearchParams();
        data.append('username', app.username);
        data.append('password', app.password);
        axios.post('login', data
        )
        .then(function (response) {
            console.log(response);
            app.message = 'Logged in.';
            app.messageIsSuccess = true;
            app.messageIsHidden = false;
            app.messageIsError = !app.messageIsSuccess;
        })
        .catch(function (error) {
            app.message = error.response.data;
            app.messageIsHidden = false;
            app.messageIsError = true;
            app.messageIsSuccess = !app.messageIsError;
            console.log(error.response.data);     
        })
    }
  },
  delimiters: ['[[',']]']
})


$('.ui.form')
  .form({
    fields: {
      username : 'empty',
      password : ['minLength[6]', 'empty']
    }
  })
;