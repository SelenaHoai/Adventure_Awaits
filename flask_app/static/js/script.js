const attractionInputs = document.getElementById('attraction')
const btn = document.getElementById('btn')


btn.addEventListener('click', (e) => {
    let input = document.createElement('input')
    input.name = "name"
    input.className="mx-1 my-3"
    input.type = "text"
    input.placeholder = "Attraction Name"

    attractionInputs.appendChild(input)
})

console.log('test')