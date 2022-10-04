let url = '/cart/process_order/';
let form = document.getElementById('shipping-info-form');
let pay_button = document.querySelector('.pay');
let shipping_radio = document.getElementById('shipping');
let pickup_radio = document.getElementById('pickup');
let shipping_div = document.querySelector('.shipping-info');
let pickup_div = document.querySelector('.pickup-info');
let email_input = document.getElementById("email");
let mobile_input =  document.getElementById("mobile-no");
let city_town_area_input = document.getElementById("city-town-area");
let delivery_pickup_radio = document.getElementsByName("shipping-or-pickup");
let desktop_email_phone_error_span = document.getElementById('email-or-phone-error');
let city_town_area_error_span = document.getElementById('city-area-error');
let mobile_email_error_span = document.getElementById("m-email-error");
let mobile_number_error_span = document.getElementById("m-mobile-error");
let radio_selection_error_span = document.getElementById("shipping-or-pickup-selection");
let shipping_option = document.getElementById('shipping_option');
let pickup_option = document.getElementById('pickup_option');
let pickup_total = document.getElementById('pickup-hidden-total-field');
let shipping_total = document.getElementById('shipping-hidden-total-field');

let total = 0;

let viewportWidth = window.innerWidth;


form.addEventListener('submit',(e)=>{
    e.preventDefault();
    
    if(delivery_pickup_radio[0].checked){
        if(city_town_area_input.value === ""){
            city_town_area_error_span.classList.add("show");
            city_town_area_error_span.innerHTML = "City, town or area is required";
            callTimeout(city_town_area_error_span);
            return false;
        }
    }
    
    if(validateEmail(email_input) && validateMobile(mobile_input)){
        document.querySelector('.continue').classList.add('hidden');
        document.querySelector('.payment-method-wrapper').style.display = "block";
    }
})


pay_button.addEventListener('click', ()=>{
    submitFormData();
})

function submitFormData(){
    let personalInfo = {
        "first_name":null,
        "last_name":null,
        "email":null,
        "total":parseFloat(total.replace(/,/g, '')),
    }

    let shippingInfo = {
        "city_town_area":null,
        "street_lane_other":null,
        "apartment_suite_building":null,
        "mobile_no":null
    }

    if( user == "AnonymousUser"){
        personalInfo.first_name = form.first_name.value
        personalInfo.last_name = form.last_name.value
        personalInfo.email = form.email.value
        shippingInfo.mobile_no = form.mobile_no.value
        shippingInfo.apartment_suite_building = form.apartment_suite_building.value
        shippingInfo.street_lane_other = form.street_lane_other.value
        shippingInfo.city_town_area = form.city_town_area.value
    }
    else{
        shippingInfo.mobile_no = form.mobile_no.value
        shippingInfo.apartment_suite_building = form.apartment_suite_building.value
        shippingInfo.street_lane_other = form.street_lane_other.value
        shippingInfo.city_town_area = form.city_town_area.value
    }


    fetch(url, {
            method:'POST',
            headers:{'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body:JSON.stringify({'personal_info':personalInfo, 'shipping_info': shippingInfo })
        })
            .then((response) =>{
            return response.json();
            })
            .then((data) =>{
            alert('Transaction completed');
            /* use better notification methods get a better response message from the backend */

            cart = {};
            document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
            location.replace("/");
        })

}

/* show and hide pickup and delivery options*/
shipping_radio.addEventListener('click', ()=>{
    shipping_div.classList.add("show");
    shipping_option.classList.add('show');
    pickup_option.classList.remove('show');
    pickup_div.classList.remove('show');
    total = shipping_total.dataset.shipping_total ;
    
})

pickup_radio.addEventListener('click', ()=>{
    shipping_div.classList.remove("show");
    shipping_option.classList.remove('show');
    pickup_div.classList.add('show');
    pickup_option.classList.add('show');
    total = pickup_total.dataset.pickup_total;
})

function validateEmail(email_field){
    let pattern = /^[A-Za-z0-9_'.-]+@[A-Za-z0-9.-]+$/i;
    if(email_field.value.match(pattern)){
        return true;
    }
    else{
        if(viewportWidth > 768){
            desktop_email_phone_error_span.classList.add('show');
            desktop_email_phone_error_span.innerHTML = "Email is not valid, please check & try again.";
            callTimeout(desktop_email_phone_error_span);
            return false;
        }
        if(viewportWidth < 768){
            mobile_email_error_span.classList.add('show');
            mobile_email_error_span.innerHTML ="Email is not valid, please check & try again";
            callTimeout(mobile_email_error_span);
            return false;
        }
    }
}

function validateMobile(mobile_field){
    /* validate if it is a safaricom number*/
    let number_pattern = /^(?:254|\+254|0)?((?:(?:7(?:(?:[01249][0-9])|(?:5[789])|(?:6[89])))|(?:1(?:[1][0-5])))[0-9]{6})$/i;
    if(mobile_field.value.match(number_pattern)){
        return true;
    }
    else {
        if(viewportWidth > 768){
            desktop_email_phone_error_span.classList.add('show');
            desktop_email_phone_error_span.innerHTML = "Please enter a valid safaricom no.";
            callTimeout(desktop_email_phone_error_span);
            return false;
        }

        if(viewportWidth < 768){
            mobile_number_error_span.classList.add("show");
            mobile_number_error_span.innerHTML = "Please enter a valid safaricom no.";
            callTimeout(mobile_number_error_span);
            return false;
        } 
    }  
} 
   

/* timeout for notifications */
function callTimeout(el){
    setTimeout(()=>{
    el.classList.remove('show');
    el.innerHTML = "";
    },5000, el);
}