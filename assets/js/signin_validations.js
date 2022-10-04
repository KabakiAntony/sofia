let form = document.getElementById('signin-form');
let email_input = document.getElementById('signin-email');
let password_input = document.getElementById('signin-password');
let email_error_span = document.getElementById('email-error');
let password_error_span = document.getElementById('password-error');

    form.addEventListener('submit',(e)=>{
        validateEmail(email_input, e);
        validatePassword(password_input, e);
    })

    /* validate email string */
    function validateEmail(email_field, event){
        let pattern = /^[A-Za-z0-9_'.-]+@[A-Za-z0-9.-]+$/i;
        if(email_field.value.match(pattern)){
        return true;
        }
        else{
        email_error_span.classList.add('show');
        email_error_span.innerHTML ="Email is not valid, please check & try again";
        event.preventDefault();
        callTimeout(email_error_span);
        return false;
        }
    }

    /* validate password string */
    function validatePassword(password_field, event){

        if(password_field.value === ""){
        event.preventDefault();
        password_error_span.classList.add('show');
        password_error_span.innerHTML = "You have not entered a password, enter one & try again.";
        callTimeout(password_error_span);
        return false;
        }
        
        if(password_field.value.length < 6){
        event.preventDefault();
        password_error_span.classList.add('show');
        password_error_span.innerHTML = "Password is too short, the minimum number of characters allowed is 6.";
        callTimeout(password_error_span);
        return false;
        }
    }

    function callTimeout(el){
        setTimeout(()=>{
        el.classList.remove('show');
        el.innerHTML = "";
        },5000, el);
    }