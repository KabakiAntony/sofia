let form = document.getElementById('signup-form');
let email_input = document.getElementById('id_email');
let password_one_input = document.getElementById('id_password1');
let password_two_input = document.getElementById('id_password2');
let email_error_span = document.getElementById('email');
let password_one_error_span = document.getElementById('password1');
let password_two_error_span = document.getElementById('password2');
let first_name_input = document.getElementById('id_first_name');
let last_name_input = document.getElementById('id_last_name');
let first_name_error_span = document.getElementById('first_name');
let last_name_error_span = document.getElementById('last_name');

    form.addEventListener('submit',(e)=>{
        validateEmail(email_input, e);
        validatePassword(password_one_input, password_two_input, e);
        validateNames(first_name_input, last_name_input, e);
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
    function validatePassword(password_one_field, password_two_field, event){

        if(password_one_field.value === ""){
            event.preventDefault();
            password_one_error_span.classList.add('show');
            password_one_error_span.innerHTML = "You have not entered a password, enter one & try again.";
            callTimeout(password_one_error_span);
            return false;
            }

        if (password_two_field.value === ""){
            event.preventDefault();
            password_two_error_span.classList.add('show');
            password_two_error_span.innerHTML = "You have not entered a password, enter one & try again.";
            callTimeout(password_two_error_span);

            return false;
            }
            
        if(password_one_field.value.length < 6 ){
            event.preventDefault();
            password_one_error_span.classList.add('show');
            password_one_error_span.innerHTML = "Password is too short, the minimum number of characters allowed is 6.";
            callTimeout(password_one_error_span);
            return false;
            }

        if( password_two_field.value.length < 6){
            event.preventDefault();
            password_two_error_span.classList.add('show');
            password_two_error_span.innerHTML = "Password is too short, the minimum number of characters allowed is 6.";
            callTimeout(password_two_error_span);
            return false;
            }

        if(password_one_field.value !== password_two_field.value){
            event.preventDefault();
            password_two_error_span.classList.add('show');
            password_two_error_span.innerHTML = "The passwords don't match, change & try again.";
            callTimeout(password_two_error_span);
            return false;
        }
    }

    function validateNames(first_name_field, last_name_field, event){
        if(first_name_field.value ===""){
            event.preventDefault();
            first_name_error_span.classList.add('show');
            first_name_error_span.innerHTML = "The firstname is required";
            callTimeout(first_name_error_span);
            return false;
        }
        if(last_name_field.value ===""){
            event.preventDefault();
            last_name_error_span.classList.add('show');
            last_name_error_span.innerHTML = "The lastname is required";
            callTimeout(last_name_error_span);
            return false;
        }
    }

    function callTimeout(el){
        setTimeout(()=>{
        el.classList.remove('show');
        el.innerHTML = "";
        },5000, el);
    }