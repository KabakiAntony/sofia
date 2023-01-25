let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
} 

let selected_color = document.getElementById('selected-id');
let  radio_buttons = document.getElementsByName('color-options');
let append_div = document.getElementById('append_product')


function change_product(sku){
    let url = '/products/select/'

      fetch(url, {
        method:'POST',
        credentials:'same-origin',
        headers:{
          "Accept": 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'sku':sku})
      })
      .then(response => response.json())
      .then(data =>{
        append_div.innerHTML = `${data.rendered_product}`;

        let slides = document.getElementsByClassName("mySlides");
        slides[0].style.display = "block";
      })
}

document.body.addEventListener('change', function(e){
  let sku = e.target.value;
  change_product(sku);

})
