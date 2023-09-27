import { showAnonMessage }  from './page/utils.js'


const dropdownMenu = document.querySelector(".dropdown-content");
const dropdownButton = document.querySelector(".dropdown-button");
let messages = document.querySelector(".messages");
let submit_buttons = document.getElementsByClassName('btn');
let anon_message = "";
let append_product_div = document.getElementById('append_product');

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

if(messages){
  setTimeout(()=>{
    messages.style.display = "none"
  }, 5000)
}

 
if (append_product_div){
  append_product_div.addEventListener('click', function(e){
    if(e.target.classList.contains('update-cart')){
  
      let entry_sku = e.target.dataset.product;
      let action = e.target.dataset.action;
      let detail_pg_product_name = document.getElementById('product-name').dataset.product_name;
      let cart_pg_product_name = e.target.dataset.product_name;
      let product_name = "";
      
      product_name = detail_pg_product_name || cart_pg_product_name;
  
      if(user === "AnonymousUser"){
 
        updateAnonymousCart(entry_sku,product_name,action);
  
      } else {
  
        updateLoggedInUserCart(entry_sku,action);
      }
  
    }
  })
}

/* add loading icon to various buttons */
for(let j=0; j< submit_buttons.length; j++){
  submit_buttons[j].addEventListener('click', function(){
    this.innerHTML = "";
    this.classList.add('submitting');
  })
}

/* update cart for authenticated users */
function updateLoggedInUserCart(sku, update_action){
  let url = '/cart/update/';

  fetch(url, {
    method:'POST',
    headers:{'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
    body:JSON.stringify({ 'entry_sku':sku, 'action': update_action })
  })
    .then((response) =>{
      return response.json();
    })
    .then((data) =>{    
      location.reload();
      /* use ajax to update cart totals without having to reload 
      the page, this works right not but it is a dirty hack*/
   })
}


/* update cart for un-authenticated users */
function updateAnonymousCart(entry_sku, productName, action){

	if (action == 'add'){
		if (cart[entry_sku] == undefined){
      cart[entry_sku] = {'quantity':1}      
		}else{
			cart[entry_sku]['quantity'] += 1
		}
    anon_message= `${productName} added successfully.`;
    showAnonMessage('success', anon_message);
	}

	if (action == 'remove'){
		cart[entry_sku]['quantity'] -= 1

		if (cart[entry_sku]['quantity'] <= 0){
			delete cart[entry_sku];
		}
    anon_message = `${productName} removed.`;
    showAnonMessage('error', anon_message);
	}

  if (action == 'delete'){
    delete cart[entry_sku];
    anon_message = `${productName} removed entirely.`;
    showAnonMessage('error', anon_message);
  }
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload();
  /*
  use ajax to get the cart total without having to 
  reload the page, right now this works but it is a 
  dirty hack
  */
}


