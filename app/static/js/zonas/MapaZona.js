const initialLat = -34.9187
const initialLng = -57.956
const mapLayerUrl = 'https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=OzyKbXmvXxFkPLosWDvP'


export class MapaZona {

    constructor({selector} , coordenadas){

        this.#initializeMap(selector, coordenadas);

    }

    #initializeMap(selector, coordenadas){
        this.map = L.map(selector).setView([initialLat,initialLng], 11);
        L.tileLayer(mapLayerUrl).addTo(this.map);

        L.polygon(coordenadas,{color:color}).addTo(this.map);

    }
}