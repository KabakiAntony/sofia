const dropdownMenu = document.querySelector(".dropdown-menu");
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


for (i=0; i< update_buttons.length; i++){
    update_buttons[i].addEventListener('click', function(){
    let product_id = this.dataset.product;
    let action = this.dataset.action;

    if(user === "AnonymousUser"){
        console.log('not logged in');
    } else {
      updateCart(product_id,action);
    }

  })
}

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
   })
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

