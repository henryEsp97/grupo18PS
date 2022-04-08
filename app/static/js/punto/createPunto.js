
import { Map } from './MapSingleMarker.js';

const submitHandler = (event, map) => {
    if(!map.marker) {
        event.preventDefault();
        alert('debes seleccionar una ubicación en el mapa');
    }
    else{
        let latlng = map.marker.getLatLng();
        document.getElementById('lat').setAttribute('value',latlng.lat);
        document.getElementById('lng').setAttribute('value',latlng.lng);
    }
}

window.onload = () => {
    const map = new Map({
        selector: 'mapid'
    }, punto
    );
    const form = document.getElementById('id-form');
    form.addEventListener('submit',(event) => submitHandler(event,map));
}