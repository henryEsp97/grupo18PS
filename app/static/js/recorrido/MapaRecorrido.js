const initialLat = -34.9187
const initialLng = -57.956
const mapLayerUrl = 'https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=OzyKbXmvXxFkPLosWDvP'


export class MapaRecorrido {
    #drawnItems;
    #recorrido;

    constructor({selector}){
        this.#drawnItems = new L.FeatureGroup();

        this.#initializeMap(selector)
        this.map.on(L.Draw.Event.CREATED, (e) =>{
            this.#eventHandler(e, this.map, this.#drawnItems, this.editControls, this.createControls)
        });
        this.map.on('draw:deleted', () =>{
            this.#deleteHandler(this.map, this.editControls, this.createControls)
        });
        this.map.on('draw:drawstop', () =>{
            this.#editHandler(this.map, this.editControls, this.createControls)
        });

    }

    #initializeMap(selector){
        this.map = L.map(selector).setView([initialLat,initialLng], 13);
        L.tileLayer(mapLayerUrl).addTo(this.map);

        if(coord){
            this.#recorrido = L.polyline(coord).addTo(this.map);
        }

        this.map.addLayer(this.#drawnItems);

        this.map.addControl(this.createControls);
    }

    #eventHandler(e, map, drawnItems, editControls, createControls){
        const existingRecorrido = Object.values(this.#drawnItems._layers);
        if (existingRecorrido.length == 0){
            const layer = e.layer;
            layer.editing.enable();
            drawnItems.addLayer(layer);
            editControls.addTo(map);
            createControls.remove();
        }        
    }

    #editHandler(map, editControls, createControls){
        editControls.addTo(map);
        createControls.remove();
        if(this.#recorrido){
            this.#recorrido.remove();
            this.map.addLayer(this.#drawnItems);
        }
    }

    #deleteHandler(map, editControls, createControls) {
        createControls.addTo(map);
        editControls.remove();
    }

    hasValidRecorrido() {
        return this.drawnlayers.length >= 3;
    }

    get drawnlayers() {
        return this.#drawnItems.getLayers()[0].getLatLngs().flat();
    }

    get editControls() {
        return this.editControlsToolbar ||= new L.Control.Draw({
            draw: false,
            edit: {
                featureGroup: this.#drawnItems
            }
        });
    }

    get createControls() {
        return this.createControlsToolbar ||= new L.Control.Draw({
            draw: {
                circle: false,
                marker: false,
                polygon: false,
                rectangle: false,
                circlemarker:false,
                polyline: true,
            }
        });
    }
}
