let append_to_div = document.getElementById('append_here');
let profile_cta = document.getElementById('profile-cta');

function get_customer_info(){
    let url = '/customers/information/'

    fetch(url,{
        method:'GET',
        credentials:'same-origin',
        headers:{"Accept": 'application/json','X-CSRFToken':csrftoken}})
        .then(response => response.json())
        .then(data =>{
            append_to_div.innerHTML =`${data.customer}`
        })
}

window.onload = function(){
    get_customer_info();

    if (profile_cta){
        profile_cta.classList.add('submitting');
    }
}
