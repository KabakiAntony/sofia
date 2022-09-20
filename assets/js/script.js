const dropdownMenu = document.querySelector(".dropdown-content");
const dropdownButton = document.querySelector(".dropdown-button");
let messages = document.querySelector(".messages");
let update_buttons = document.getElementsByClassName('update-cart');

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


/* cannot use an arrow function here since 
'this' does not bind to an arrow function */
for (let i=0; i< update_buttons.length; i++){
    update_buttons[i].addEventListener('click', function(){
    let product_id = this.dataset.product;
    let action = this.dataset.action;

    console.log(this.dataset.product)

    if(user === "AnonymousUser"){
      addCookieItem(product_id,action);
    } else {
      updateCart(product_id,action);
    }

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
function addCookieItem(productId, action){
	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}
    /* show messages using js*/

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			delete cart[productId];
		}
	}

  if (action == 'delete'){
    delete cart[productId];
  }
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
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

