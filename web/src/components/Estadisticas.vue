<template>
  <div>
    <h2 style="display:flex; justify-content: center">Estadísticas</h2>
    <div>
      <h2>Cantidad de denuncias:</h2>
      <h4>&emsp;{{estadisticas[0].cantidad_denuncias}}</h4>
      <h2>Cantidad de puntos de encuentro:</h2>
      <h4>&emsp;{{estadisticas[0].cantidad_puntos}}</h4>
      <h2>Cantidad de recorridos de evacuación:</h2>
      <h4>&emsp;{{estadisticas[0].cantidad_recorridos}}</h4>
      <h2>Cantidad de zonas inundables:</h2>
      <h4>&emsp;{{estadisticas[0].cantidad_zonas_inundables}}</h4>
    </div>
  </div>
</template>
<script>
export default {
  data () {
    return {
      estadisticas: {}
    }
  },
  async created () {
    try {
      const response = await fetch('https://admin-grupo18.proyecto2021.linti.unlp.edu.ar/api/estadisticas/')
      const json = await response.json()
      this.estadisticas = json
    } catch (e) {
      alert(e)
    }
  }
}
</script>
