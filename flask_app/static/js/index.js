function initMap() {
    const uluru = {lat:47.6062,lng:-122.3321};
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: uluru,
    });
    const marker = new google.maps.Marker({
        position: uluru,
        map: map,
    });
}

window.initMap = initMap;