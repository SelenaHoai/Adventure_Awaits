const attractionInputs = document.getElementById('attraction')
const btn = document.getElementById('btn')


btn.addEventListener('click', (e) => {
    let input = document.createElement('input')
    input.name = "name"
    input.className="my-2"
    input.type = "text"
    input.placeholder = "Attraction name"

    attractionInputs.appendChild(input)
})

console.log('test')