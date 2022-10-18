let anon_messages = document.querySelector(".anon-messages");

export function showAnonMessage(class_type, message){
    anon_messages.classList.add(class_type);
    anon_messages.innerHTML = message;
    setTimeout(()=>{
        anon_messages.classList.remove(class_type);
        anon_messages.innerHTML = "";
      }, 5000, class_type)
}