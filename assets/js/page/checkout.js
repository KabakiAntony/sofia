import { showAnonMessage } from './utils.js';

let form = document.getElementById('shipping-info-form');
/* inputs */
let firstname_input = document.getElementById("id_firstname");
let lastname_input = document.getElementById("id_lastname");
let region_input = document.getElementById("id_region");
let area_input = document.getElementById("id_area");
let email_input = document.getElementById("id_email");
let mobile_input = document.getElementById("id_mobile_no");
let selected_area = document.getElementById('id_area');
let address_area = document.getElementById('address_area');

/* radio buttons*/
let delivery_pickup_radio = document.getElementsByName("shipping_or_pickup");
let delivery_location_radio = document.getElementsByName("delivery_location");
let shipping_radio = document.getElementById('shipping');
let pickup_radio = document.getElementById('pickup');
let address_on_file_radio = document.getElementById('address_on_file');
let set_new_address_radio = document.getElementById('set_new_address');

/* divs */
let shipping_div = document.querySelector('.shipping-info');
let pickup_div = document.querySelector('.pickup-info');
let address_on_file_div = document.querySelector('.address-on-file');
let set_new_address_div = document.querySelector('.set-new-address');
let desktop_name_error_div = document.getElementById('desktop-errors-name');
let desktop_email_phone_error_div = document.getElementById('desktop-errors-email-phone');

/* error labels */
let desktop_phone_error_label = document.getElementById('desktop-phoneno-error');
let desktop_email_error_label = document.getElementById('desktop-email-error');
let desktop_firstname_error_label = document.getElementById('desktop-firstname-error');
let desktop_lastname_error_label = document.getElementById('desktop-lastname-error');
let mobile_first_name_error_label = document.getElementById('mobile-firstname-error');
let mobile_last_name_error_label = document.getElementById('mobile-lastname-error');
let mobile_email_error_label = document.getElementById('mobile-email-error');
let mobile_phoneno_error_label = document.getElementById('mobile-phoneno-error');
let shipping_pickup_error_label = document.getElementById('shipping-pickup-error');
let onfile_newaddress_error_label = document.getElementById('onfile-newaddress-error');
let set_address_error_label = document.getElementById('set_address_error');

let shipping_total = document.getElementById('shipping_hidden_total_field');

let anon_message = "";
let total = "";
let viewportWidth = window.innerWidth;
let customerInfo = {}
let addressInfo = {}

/* show and hide pickup and delivery (shipping) options*/
shipping_radio.addEventListener('click', () => {
    pickup_div.classList.remove('show');
    shipping_div.classList.add("show");

    if (user !== "AnonymousUser") {
        set_new_address_div.classList.remove('show');
        address_on_file_div.classList.remove('show');
    }
})

pickup_radio.addEventListener('click', () => {
    shipping_div.classList.remove("show");
    pickup_div.classList.add('show');

    if (user !== "AnonymousUser") {
        set_new_address_div.classList.remove('show');
        address_on_file_div.classList.remove('show');
    }
    get_pickup_id();
})

if (user !== "AnonymousUser") {

    address_on_file_radio.addEventListener('click', () => {
        address_on_file_div.classList.add('show');
        set_new_address_div.classList.remove('show');
        let area_id = address_area.dataset.address_area_id;
        get_shipping_cost(area_id);
    })

    set_new_address_radio.addEventListener('click', () => {
        address_on_file_div.classList.remove('show');
        set_new_address_div.classList.add('show');
    })
}


if (selected_area) {
    selected_area.addEventListener('change', (e) => {
        let area_id = e.target.value;
        get_shipping_cost(area_id);
    })
}


function deliveryOrPickup(){
    shipping_pickup_error_label.classList.add('show');
    shipping_pickup_error_label.innerHTML = "Please select either Delivery or Pickup";
    callTimeout(shipping_pickup_error_label);
    return false;
}

/* timeout for notifications */
function callTimeout(el) {
    setTimeout(() => {
        el.classList.remove('show');
        el.innerHTML = "";
    }, 7000, el);
}

/* 
    get shipping cost depending on what 
    area and region the user has selected
*/
function get_shipping_cost(id) {
    let url = '/get-shipping-cost/';
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'area_id': id })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("shipping_option").innerHTML = `${data.rendered_total}`;

            total = document.getElementById('shipping_hidden_total_field').getAttribute('data-total');
        })
}

// get an id for the cbd pickup option
function get_pickup_id() {
    let url = '/get-pickup-id/';
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
        .then(response => response.json())
        .then(data => {
            get_shipping_cost(data.area_id);
        })
}

/* enable pay button and disable continue button on validation pass*/
function enablePayBtnDisableContinueBtn(){
    document.querySelector('.continue').classList.add('hidden');
    document.querySelector('.payment-method-wrapper').style.display = "block";
    return true;
}

function checkRegionAreaFill(){
    if(!region_input.value.trim() && !area_input.value.trim()){
        region_input.style.border = '1px solid #e71809';
        area_input.style.border = '1px solid #e71809';
        set_address_error_label.classList.add('show');
        set_address_error_label.innerHTML = "Please set a delivery address";
        callTimeout(set_address_error_label);
        return false;
    } else if (region_input.value.trim() && area_input.value.trim()){
        enablePayBtnDisableContinueBtn();
    }

}

function checkPersonalInfo(){

    if (!firstname_input.value.trim()){
        if (viewportWidth > 768){
            desktop_firstname_error_label.classList.add('show');
            desktop_firstname_error_label.innerHTML = "Please enter a firstname";
            callTimeout(desktop_firstname_error_label);
            
        } else if ( viewportWidth < 768){
            mobile_first_name_error_label.classList.add('show');
            mobile_first_name_error_label.innerHTML = "Please enter a firstname";
            callTimeout(mobile_first_name_error_label);
        }
    } 

    if(!lastname_input.value.trim()){

        if (viewportWidth > 768){
            desktop_lastname_error_label.classList.add('show');
            desktop_lastname_error_label.innerHTML = "Please enter a lastname";
            callTimeout(desktop_lastname_error_label);

        } else if ( viewportWidth < 768){
            mobile_last_name_error_label.classList.add('show');
            mobile_last_name_error_label.innerHTML = "Please enter a lastname";
            callTimeout(mobile_last_name_error_label);
        }
    }

    if(!email_input.value.trim()){

        if (viewportWidth > 768){
            desktop_email_error_label.classList.add('show');
            desktop_email_error_label.innerHTML = "Please enter an email";
            callTimeout(desktop_email_error_label);
            
        } else if ( viewportWidth < 768){
            mobile_email_error_label.classList.add('show');
            mobile_email_error_label.innerHTML = "Please enter an email";
            callTimeout(mobile_email_error_label);
        }

    } else {
        /* validate email */
    }

    if(!mobile_input.value.trim()){

        if (viewportWidth > 768){
            desktop_phone_error_label.classList.add('show');
            desktop_phone_error_label.innerHTML = "Please enter an mpesa mobile no";
            callTimeout(desktop_phone_error_label);

        } else if ( viewportWidth < 768){
            mobile_phoneno_error_label.classList.add('show');
            mobile_phoneno_error_label.innerHTML = "Please enter an mpesa mobile no";
            callTimeout(mobile_phoneno_error_label);
        }

    } else {
        /* validate mobile no */
    }

}

function deliverToNewOrOnFile(){
    if(!set_new_address_radio.checked && !address_on_file_radio.checked){
        onfile_newaddress_error_label.classList.add('show');
        onfile_newaddress_error_label.innerHTML = "Please select either Setting new address or On file address";
        callTimeout(onfile_newaddress_error_label);
        return false;

    } else if (set_new_address_radio.checked){
        checkRegionAreaFill();

    } else if(address_on_file_radio.checked){
        enablePayBtnDisableContinueBtn();

    }
}

/* check inputs for authenticated user */
function checkInputsForLoggedInUser(){
    if(!shipping_radio.checked && !pickup_radio.checked){

        deliveryOrPickup();

    } else if (shipping_radio.checked){

        deliverToNewOrOnFile();

    } else if (pickup_radio.checked) {
        /* selected pickup */
        enablePayBtnDisableContinueBtn();
    }
}

function checkInputsForAnonymous(){
    checkPersonalInfo();

    if(!shipping_radio.checked && !pickup_radio.checked){

        deliveryOrPickup();

    } else if (shipping_radio.checked){
        /* check if other inputs are filled */
        checkRegionAreaFill();

    } else if (pickup_radio.checked) {
        /* selected pickup */
        /* check if other inputs are filled */
        enablePayBtnDisableContinueBtn();
    }
}

function userData() {

    if (user == "AnonymousUser") {
        // you are a guest user

        if (delivery_pickup_radio[0].checked) {
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
        }
        else {
            // you have selected to pickup 
            customerInfo.first_name = form.firstname.value
            customerInfo.last_name = form.lastname.value
            customerInfo.email = form.email.value
            addressInfo.mobile_no = form.mobile_no.value
            addressInfo.shipping_or_pickup = form.shipping_or_pickup.value
            customerInfo.total = parseFloat(total.replace(/,/g, ''));
        }
    }
    else {

        if (delivery_pickup_radio[0].checked) {
            // you are logged in and you have selected to deliver
        
            if (delivery_location_radio[0].checked) {
                // you have selected to deliver to address on file
                customerInfo.total = parseFloat(total.replace(/,/g, ''));
                addressInfo.shipping_or_pickup = form.shipping_or_pickup.value;
                addressInfo.delivery_address = form.delivery_location.value;
            }

            if (delivery_location_radio[1].checked) {
                // you have selected to set a new delivery address
                customerInfo.total = parseFloat(total.replace(/,/g, ''));
                addressInfo.apartment_suite_building = form.apartment_suite_building.value;
                addressInfo.street_lane_other = form.street_lane_other.value;
                addressInfo.region = form.region.value;
                addressInfo.area = form.area.value;
                addressInfo.shipping_or_pickup = form.shipping_or_pickup.value;
                addressInfo.delivery_address = form.delivery_location.value;
            }
        }
        else {
            // you are logged in and you have selected pickup
            customerInfo.total = parseFloat(total.replace(/,/g, ''));
            addressInfo.shipping_or_pickup = form.shipping_or_pickup.value;
            addressInfo.delivery_address = form.delivery_location.value;
        }
    }
    return {
        "customer_info": customerInfo,
        "address_info": addressInfo
    }

}


function submitFormData(){
    let url = '/process_order/';
    let user_data = userData();
    customerInfo = user_data.customer_info
    addressInfo = user_data.address_info

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: JSON.stringify({ 'customer_info': customerInfo, 'address_info': addressInfo })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {

            if (data === 201) {
                anon_message = "Please check your mpesa phone for a payment request from Safaricom on our behalf."
                showAnonMessage("info", anon_message);
                cart = {};
                document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
                location.replace("/payment-status/");
            }
        })
}

/* click on either the continue or pay button */
document.body.addEventListener('click', (e) => {
    
    if (e.target.id === 'continue-btn') {
        e.preventDefault();

        /* validate depending on user instance */
        if( user !== "AnonymousUser"){
            /* logged in user */
            checkInputsForLoggedInUser();

        } else {
            /* anonymous user (guest)*/
            checkInputsForAnonymous();
            
        }

    }

    if (e.target.id === 'pay-btn') {
        submitFormData();
    }
});