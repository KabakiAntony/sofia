const dropdownMenu = document.querySelector(".dropdown-content");
const dropdownButton = document.querySelector(".dropdown-button");
let messages = document.querySelector(".messages");
let anon_messages = document.querySelector(".anon-messages");
let update_buttons = document.getElementsByClassName('update-cart');
let submit_buttons = document.getElementsByClassName('btn');


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

function unloadAnonMessages(class_type){
  if(anon_messages){
    setTimeout(()=>{
      anon_messages.classList.remove(class_type);
    }, 5000, class_type)
  }
}

/* 
cannot use an arrow function here since 
'this' does not bind to an arrow function
*/
for (let i=0; i< update_buttons.length; i++){
    update_buttons[i].addEventListener('click', function(){
    let product_id = this.dataset.product;
    let action = this.dataset.action;
    let product_name = document.getElementById('product-name').dataset.product_name;

    if(user === "AnonymousUser"){
      addCookieItem(product_id,product_name,action);
    } else {
      updateCart(product_id,action);
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
function updateCart(productId, update_action){
  let url = '/cart/update/';

  fetch(url, {
    method:'POST',
    headers:{'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
    body:JSON.stringify({ 'product_id':productId, 'action': update_action })
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
function addCookieItem(productId, productName, action){
	if (action == 'add'){
		if (cart[productId] == undefined){
      cart[productId] = {'quantity':1}      
		}else{
			cart[productId]['quantity'] += 1
		}
    anon_messages.classList.add('success');
    anon_messages.innerHTML = `1 unit of ${productName} added successfully.`;
    unloadAnonMessages('success');
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			delete cart[productId];
		}
    anon_messages.classList.add('error');
    anon_messages.innerHTML = `1 unit of ${productName} removed.`;
    unloadAnonMessages('error');
	}

  if (action == 'delete'){
    delete cart[productId];
    anon_messages.classList.add('error');
    anon_messages.innerHTML = `${productName} removed entirely.`;
    unloadAnonMessages('error');
  }
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	 location.reload();
  /*
  use ajax to get the cart total without having to 
  reload the page, right now this works but it is a 
  dirty hack
  */
}

// // Upload Image
// const photoInput = document.querySelector("#avatar");
// const photoPreview = document.querySelector("#preview-avatar");
// if (photoInput)
//   photoInput.onchange = () => {
//     const [file] = photoInput.files;
//     if (file) {
//       photoPreview.src = URL.createObjectURL(file);
//     }
//   };

