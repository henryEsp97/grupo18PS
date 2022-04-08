<template>
  <div class="container mt-5">
  <div class="row">
    <div class="col-sm-4">
      <div class="conteiner-info">
        <h2 class="mt-5">
          <router-link to="/denuncias-ver" class="nav-link">Ver denuncias</router-link>
        </h2>
        <div class="fakeimg">Fake Image</div>
        <p>Aqui encontrara todo acerca sobre denuncias.</p>
      </div>
      <div class="conteiner-info">
        <h2 class="mt-5">
          <router-link to="/denuncias-carga" class="nav-link">Realizar Denuncia</router-link>
        </h2>
        <p>Si desea realizar una denuncia ingrese.</p>
      </div>
      <div class="conteiner-info">
        <h2 class="mt-5">
          <router-link to="/Estadisticas" class="nav-link">Estadísticas</router-link>
        </h2>
        <p>Seccion de estadisticas</p>
      </div>
    </div>
    <div class="col-sm-8">
      <div class="conteiner-info">
        <h2 class="mt-5">
          <router-link to="/puntosRecorridos" class="nav-link">Puntos de encuentro y sus reccoridos</router-link>
        </h2>
        <div class="fakeimg">Fake Image</div>
        <p>Aca encontrara el reccorido al punto de encuentro mas cercano en caso de emergencia.</p>
      </div>
      <div class="conteiner-info">
        <h2 class="mt-5">
          <router-link to="/zonas-inundables" class="nav-link">Zonas inundables</router-link>
        </h2>
        <p>Información y visualización de las zonas inundables de La Plata.</p>
        <!-- <img src="../../../app/static/img/mapa.png"> -->
      </div>
    </div>
  </div>
</div>
</template>
