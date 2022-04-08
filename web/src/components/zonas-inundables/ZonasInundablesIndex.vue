<template>
<div>
  <form class="form">
    <l-map style="height: 300px" :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <div v-for="(zona) in zonas" :key="zona.id">
        <l-polygon :lat-lngs="zona.coordenadas" :color="zona.color" :fill="true" :fillColor="zona.color">
          <l-popup>{{zona.nombre}}</l-popup>
        </l-polygon>
        {{zona.nombre}}
      </div>
    </l-map>
    <ul>
      <li v-for="(zona) in zonas" :key="zona.id">
        {{zona.nombre}}
        <router-link :to= "{ name: 'zonas-inundables-ver', params: { id: zona.id }}" class="link">Ver detalles</router-link>
      </li>
    </ul>
  </form>
</div>
</template>

<script>
import { LMap, LTileLayer, LPolygon, LPopup } from '@vue-leaflet/vue-leaflet'

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
      zonas: []
    }
  },
  async created () {
    //  hace la petición a la api
    try {
      const response = await fetch('https://admin-grupo18.proyecto2021.linti.unlp.edu.ar/api/zonas-inundables/all')
      const json = await response.json()
      this.zonas = json.zonas
    } catch (e) {
      alert(e)
    }
    //  centra el mapa en la localización del usuario
    if ('geolocation' in navigator) {
      var self = this
      navigator.geolocation.getCurrentPosition(function (position) {
        self.center = [position.coords.latitude, position.coords.longitude]
      })
    } else {
      alert('Para centrar el mapa en su zona, habilite la localización de su navegador')
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
