// Update Page

const attractionInputsUpdate = document.getElementById('attraction-update')
const btnUpdate = document.getElementById('btn-update')


btnUpdate.addEventListener('click', (e) => {
    let input = document.createElement('input')
    input.name = "name_new"
    input.className="mx-1 my-3"
    input.type = "text"
    input.placeholder = "Attraction Name"

    attractionInputsUpdate.appendChild(input)
})