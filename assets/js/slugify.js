const roomNameInput = document.querySelector('input[name=name]');
const roomSlugInput = document.querySelector('input[name=slug]');

const slugify = (val) =>{
    return val.toString().toLowerCase().trim()
    .replace(/&/g, '-and-') // replace & with '-and-'
    .replace(/[\s\W-]+/g,'-') // replace spaces, non word chars and dashes with '-'
};

roomNameInput.addEventListener('keyup',(e)=>{
  roomSlugInput.setAttribute('value', slugify(roomNameInput.value));
})