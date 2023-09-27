import { showAnonMessage }  from './utils.js';

let url = '/cart/process_order/';
let form = document.getElementById('shipping-info-form');
// let pay_button = document.querySelector('.pay');
let shipping_radio = document.getElementById('shipping');
let pickup_radio = document.getElementById('pickup');
let shipping_div = document.querySelector('.shipping-info');
let pickup_div = document.querySelector('.pickup-info');
let email_input = document.getElementById("id_email");
let mobile_input =  document.getElementById("id_mobile_no");
// let region_input = document.getElementById("id_region");
let area_input = document.getElementById("id_area");
let delivery_pickup_radio = document.getElementsByName("shipping_or_pickup");
let delivery_method_radio = document.getElementsByName("delivery_method");
let desktop_email_phone_error_span = document.getElementById('email-or-phone-error');
// let city_town_area_error_span = document.getElementById('city-area-error');
let mobile_email_error_span = document.getElementById("m-email-error");
let mobile_number_error_span = document.getElementById("m-mobile-error");
// let shipping_option = document.getElementById('shipping_option');
// let pickup_total = document.getElementById('pickup-hidden-total-field');
let shipping_total = document.getElementById('shipping_hidden_total_field');
let address_on_file_radio = document.getElementById('address_on_file');
let set_new_address_radio = document.getElementById('set_new_address');
let address_on_file_div = document.querySelector('.address-on-file');
let set_new_address_div = document.querySelector('.set-new-address');
let selected_area = document.getElementById('id_area');
let address_area = document.getElementById('address_area');
// let continue_btn = document.getElementById('continue-btn');
let anon_message = "";
let total = "";
let viewportWidth = window.innerWidth;

let customerInfo = {
    "first_name":null,
    "last_name":null,
    "email":null,
    "total":null,
}

let addressInfo = {
    "region":null,
    "area":null,
    "street_lane_other":null,
    "apartment_suite_building":null,
    "shipping_or_pickup":null,
    "mobile_no":null,
    "delivery_address":null,
}

document.body.addEventListener('click',(e)=>{

    if(e.target.id === 'continue-btn'){
        e.preventDefault();
        
        // if(validateEmail(email_input) && validateMobile(mobile_input)){
            document.querySelector('.continue').classList.add('hidden');
            document.querySelector('.payment-method-wrapper').style.display = "block";
        // }
    }

    if (e.target.id === 'pay-btn'){
        submitFormData();
    }

    // if(delivery_pickup_radio[0].checked && user === "AnonymousUser" ){
    //     if(area_input.value === ""){
    //         city_town_area_error_span.classList.add("show");
    //         city_town_area_error_span.innerHTML = "City, town or area is required";
    //         callTimeout(city_town_area_error_span);
    //         return false;
    //     }
    // }
    
})

function submitFormData(){

    let user_data = userData();
    customerInfo = user_data.customer_info
    addressInfo = user_data.address_info

    fetch(url, {
            method:'POST',
            headers:{'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body:JSON.stringify({'customer_info':customerInfo, 'address_info': addressInfo })
            })
            .then((response) =>{
            return response.json();
            })
            .then((data) =>{
                
                if(data === 201){
                    anon_message = "Please check your mpesa phone for a payment request from Kopokopo on our behalf."
                    showAnonMessage("info", anon_message);
                    cart = {};
                    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
                    location.replace("/cart/payment-status/");
                }
        })

}

/* show and hide pickup and delivery options*/
shipping_radio.addEventListener('click', ()=>{
    pickup_div.classList.remove('show');
    shipping_div.classList.add("show");
    if(user !== "AnonymousUser"){
        set_new_address_div.classList.remove('show');
        address_on_file_div.classList.remove('show');
    }
})

pickup_radio.addEventListener('click', ()=>{
    shipping_div.classList.remove("show");
    pickup_div.classList.add('show');
    if(user !== "AnonymousUser"){
        set_new_address_div.classList.remove('show');
        address_on_file_div.classList.remove('show');
    }
    get_pickup_id();
})

if(user !== "AnonymousUser"){
    address_on_file_radio.addEventListener('click', ()=>{
        address_on_file_div.classList.add('show');
        set_new_address_div.classList.remove('show');
        let area_id = address_area.dataset.address_area_id;
        get_shipping_cost(area_id);
    })
    
    set_new_address_radio.addEventListener('click', ()=>{
        address_on_file_div.classList.remove('show');
        set_new_address_div.classList.add('show');
    })
}


if(selected_area){
    selected_area.addEventListener('change',(e)=>{
        let area_id = e.target.value;
        get_shipping_cost(area_id);
    })
  }

/* 
    get shipping cost depending on what 
    area and region the user has selected
*/
function get_shipping_cost(id){
    let url = '/customers/get-shipping-cost/';
    fetch(url, {
        method:'POST',
        credentials:'same-origin', 
        headers:{
          'Content-Type': 'application/json',
          'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'area_id':id})
      })
      .then(response => response.json())
      .then(data =>{
        document.getElementById("shipping_option").innerHTML = `${data.rendered_total}`;

        total = document.getElementById('shipping_hidden_total_field').getAttribute('data-total');
      })
}

// get an id for the cbd pickup option
function get_pickup_id(){
    let url = '/customers/get-pickup-id/';
    fetch(url, {
        method:'GET',
        credentials:'same-origin', 
        headers:{
          'Content-Type': 'application/json',
          'X-CSRFToken':csrftoken,
        }
      })
      .then(response => response.json())
      .then(data =>{
        get_shipping_cost(data.area_id);
      })
}


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

function userData(){

    if(user == "AnonymousUser" ){
        // you are a guest user

        if( delivery_pickup_radio[0].checked){
            // you have selected to have it delivered to you
            
            customerInfo.first_name = form.firstname.value;
            customerInfo.last_name = form.lastname.value;
            customerInfo.email = form.email.value;
            addressInfo.mobile_no = form.mobile_no.value;
            addressInfo.apartment_suite_building = form.apartment_suite_building.value;
            addressInfo.street_lane_other = form.street_lane_other.value;
            addressInfo.region = form.region.value;
            addressInfo.area = form.area.value;
            addressInfo.shipping_or_pickup = form.shipping_or_pickup.value;
            customerInfo.total = parseFloat(total.replace(/,/g, ''));

            return {
                "customer_info": customerInfo, 
                "address_info": addressInfo
            };
        }
        else{
            // you have selected to pickup 
            customerInfo.first_name = form.firstname.value
            customerInfo.last_name = form.lastname.value
            customerInfo.email = form.email.value
            addressInfo.mobile_no = form.mobile_no.value
            addressInfo.shipping_or_pickup = form.shipping_or_pickup.value
            customerInfo.total = parseFloat(total.replace(/,/g, ''));

            return {
                "customer_info": customerInfo, 
                "address_info": addressInfo
            };
        }
    }
    else{

        if( delivery_pickup_radio[0].checked ){
            // you are logged in and you have selected to deliver

            if(delivery_method_radio[0].checked){
                // you have selected to deliver to address on file
                
                customerInfo.total = parseFloat(total.replace(/,/g, ''));
                addressInfo.shipping_or_pickup = form.shipping_or_pickup.value;
                addressInfo.delivery_address = form.delivery_method_radio.value;

                return {
                    "customer_info": customerInfo, 
                    "address_info": addressInfo
                };
            }
            
            if(delivery_method_radio[1].checked){
                // you have selected to set a new delivery address

                customerInfo.total = parseFloat(total.replace(/,/g, ''));
                addressInfo.apartment_suite_building = form.apartment_suite_building.value;
                addressInfo.street_lane_other = form.street_lane_other.value;
                addressInfo.region = form.region.value;
                addressInfo.area = form.area.value;
                addressInfo.shipping_or_pickup = form.shipping_or_pickup.value;
                addressInfo.delivery_address = form.delivery_method_radio.value;

                return {
                    "customer_info": customerInfo, 
                    "address_info": addressInfo
                };
            }
        }
        else{
            // you are logged in and you have selected pickup

            customerInfo.total = parseFloat(total.replace(/,/g, ''));
            addressInfo.shipping_or_pickup = form.shipping_or_pickup.value;
            addressInfo.delivery_address = form.delivery_method_radio.value;

            return {
                "customer_info": customerInfo, 
                "address_info": addressInfo
            };
        }
        
    }

}

