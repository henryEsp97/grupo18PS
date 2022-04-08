<template>
<div>
  <div>
    <h1 v-if= not denuncias>No hay denuncias cargadas</h1>
    <form class="form">
        <l-map style="height: 500px" :zoom="zoom" :center="center">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <div v-for="(denuncia) in denuncias" :key="denuncia.id">
            <l-marker :lat-lng="denuncia.coordenadas[0]" >
                <l-popup>
                  <h6>{{denuncia.titulo}}</h6>
                  <h6>DESCRIPCION:{{denuncia.descripcion}}</h6>
                  <h6>CATEGORIA:{{denuncia.categoria}}</h6>
                  <h6>ESTADO:{{denuncia.estado}}</h6>
                </l-popup>
            </l-marker>
        </div>
        </l-map>
    </form>
    <div style="display:flex; justify-content:center">
      <button v-if="page>1" @click=decrement v-on:click="getData">&laquo;</button>
          <p>página:{{page}}</p>
      <button v-if= denuncias @click=increment v-on:click="getData">&raquo;</button>
    </div>
  </div>
</div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 13,
      center: [-34.9187, -57.956],
      denuncias: [],
      page: 1
    }
  },
  methods: {
    increment () {
      this.page++
    },
    decrement () {
      this.page--
    },
    async getData () {
      try {
        const response = await fetch('https://admin-grupo18.proyecto2021.linti.unlp.edu.ar/api/denuncias/paginate?page=' + this.page)
        const json = await response.json()
        this.denuncias = json.denuncias
      } catch (e) {
        alert(e)
      }
    }
  },
  async created () {
    //  centra el mapa en la localización del usuario
    if ('geolocation' in navigator) {
      var self = this
      navigator.geolocation.getCurrentPosition(function (position) {
        self.center = [position.coords.latitude, position.coords.longitude]
      })
    } else {
      alert('Para centrar el mapa en su zona, habilite la localización de su navegador')
    }
    //  hace la petición a la api con el número de página en la que esté el user
    try {
      const response = await fetch('https://admin-grupo18.proyecto2021.linti.unlp.edu.ar/api/denuncias/paginate?page=' + this.page)
      const json = await response.json()
      this.denuncias = json.denuncias
    } catch (e) {
      alert(e)
    }
  }
}
</script>

<style scoped>
.form{
text-align: center;
width: 70%;
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
