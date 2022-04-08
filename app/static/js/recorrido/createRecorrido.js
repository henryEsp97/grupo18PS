
import { MapaRecorrido } from './MapaRecorrido.js';

const submitHandler = (event, map) => {
    if(!map.hasValidRecorrido()) {
        alert('Debes seleccionar al menos 3 puntos en el mapa');
    }
    else{
        const coordinates = map.drawnlayers.map(coordinate => {
            return {lat: coordinate.lat, lng: coordinate.lng }
        });

        //convierte las coordenadas del recorrido en un string con formato [[lat1,long1],[lat2,long2],...]
        let stringListaCoordenadas = '['
        for (const cor in coordinates){
            let objetoDict = coordinates[cor];
            stringListaCoordenadas=stringListaCoordenadas.concat('[',objetoDict.lat,',',objetoDict.lng,']');
            if (cor != coordinates.length-1){
                stringListaCoordenadas+=',';
            }
        }
        stringListaCoordenadas+=']';

        //Pone el string de coordenadas en el tag input name=coord
        document.getElementById('coord').setAttribute('value',stringListaCoordenadas);
    }
}

window.onload = () =>{
    const map = new MapaRecorrido({
        selector: 'mapid',
        addSearch: true
    }, coord);

    const form =  document.getElementsByClassName("create-forms");
    form[0].addEventListener('submit',(event) => submitHandler(event,map));
}
