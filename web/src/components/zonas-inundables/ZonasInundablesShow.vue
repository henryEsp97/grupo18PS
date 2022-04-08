<template>
<div>
<form class="form">
    <l-map style="height: 300px" :zoom="zoom" :center="center">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <div>
            <l-polygon :lat-lngs="zona.coordenadas" :color="zona.color" :fill="true" :fillColor="zona.color">
                <l-popup>{{zona.nombre}}</l-popup>
            </l-polygon>
            {{zona.nombre}}
        </div>
    </l-map>
    <ul>
        <li>
            {{zona.nombre}}
        </li>
    </ul>
    <router-link to="/zonas-inundables" class="link">Volver</router-link>
</form>
</div>
</template>

<script>
import { LMap, LTileLayer, LPolygon, LPopup } from '@vue-leaflet/vue-leaflet'

//  función para calcular el centro aprox del polígono, recibe un arr [ [lat1,long1], [lat2,long2] , .. ]
function getCentro (arr) {
  return arr.reduce(function (x, y) {
    return [x[0] + y[0] / arr.length, x[1] + y[1] / arr.length]
  }, [0, 0])
}

export default {
  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LPopup
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 13,
      center: [-34.9187, -57.956],
      zona: {},
      id: 0
    }
  },
  async created () {
    this.id = this.$route.params.id //  pone como id el pasado como parámetro de la URL

    //  hace el fetch a la api
    try {
      const response = await fetch('https://admin-grupo18.proyecto2021.linti.unlp.edu.ar/api/zonas-inundables/' + this.id)
      const json = await response.json()
      this.zona = json[1]
      this.center = getCentro(this.zona.coordenadas) // centra el mapa en el centro de la zona
    } catch (e) {
      alert(e)
    }
  }
}
</script>

<style scoped>
.form{
text-align: center;
width: 40%;
height: 80%;
padding:16px;
border-radius:10px;
margin: 0 auto;
margin-top: 30px;
background-color:#ccc;
}
.link {
  text-transform: uppercase;
  font-size: 10px;
  background-color: #92a4ad;
  padding: 10px 15px;
  border-radius: 0;
  color: white;
  display: inline-block;
  margin-right: 5px;
  margin-bottom: 5px;
  line-height: 1.5;
  text-decoration: none;
  letter-spacing: 1px;
}
</style>
