import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import IniciarSesion from '../views/IniciarSesion.vue'
import ZonasInundablesIndex from '../components/zonas-inundables/ZonasInundablesIndex.vue'
import ZonasInundablesShow from '../components/zonas-inundables/ZonasInundablesShow.vue'
import Denuncias from '../components/denuncias/DenunciasCarga.vue'
import AllDenuncias from '../components/denuncias/DenunciasVer.vue'
import PuntosRecorridosIndex from '../components/puntosRecorridos/PuntosRecorridosIndex.vue'
import Estadisticas from '../components/Estadisticas.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/iniciar-sesion',
    name: 'iniciar-sesion',
    component: IniciarSesion
  },
  {
    path: '/zonas-inundables',
    name: 'zonas-inundables',
    component: ZonasInundablesIndex
  },
  {
    path: '/zonas-inundables/ver/:id',
    name: 'zonas-inundables-ver',
    component: ZonasInundablesShow
  },
  {
    path: '/denuncias-carga',
    name: 'denuncias-carga',
    component: Denuncias
  },
  {
    path: '/denuncias-ver',
    name: 'denuncias-ver',
    component: AllDenuncias
  },
  {
    path: '/puntosRecorridos',
    name: 'puntos-recorridos',
    component: PuntosRecorridosIndex
  },
  {
    path: '/estadisticas',
    name: 'estadisticas',
    component: Estadisticas
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
