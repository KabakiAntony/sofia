let selected_region = document.getElementById('id_region');
let update_address = document.getElementById('update_address');

function get_region_areas(id) {
  // let url = '/customers/areas/' old url
  let url = '/areas/'

  fetch(url, {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'region_id': id })
  })
    .then(response => response.text())
    .then(html => {
      document.getElementById("id_area").innerHTML = html;
    })
}

if (selected_region) {
  selected_region.addEventListener('change', (e) => {
    let region_id = e.target.value
    get_region_areas(region_id);

  })
}
