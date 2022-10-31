let main_image = document.getElementById("main-image");
let other_images = document.getElementsByClassName("other-image");
let domain = window.location

for (let i=0; i< other_images.length; i++){
    other_images[i].addEventListener('click', function(){
    let image_src = this.dataset.other_image_src;
    main_image.src = `${domain.origin}${image_src}`;
  })
}