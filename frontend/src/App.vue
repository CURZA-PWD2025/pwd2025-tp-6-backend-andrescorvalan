<template>
  <div class="app">
    <nav> 
      <router-link class="opcion_menu" :to="{name: 'home'}">Home</router-link>
      <router-link class="opcion_menu" :to="{name: 'marcas_list'}">Listado de Marcas</router-link>
      <router-link class="opcion_menu" :to="{name: 'proveedores_list'}">Listado de Proveedores</router-link>
      <router-link class="opcion_menu" :to="{name: 'categorias_list'}">Listado de Categorias</router-link>
      <router-link class="opcion_menu" :to="{name: 'articulos_list'}">Listado de Articulos</router-link>
    </nav>
    <router-view> </router-view>
  </div>
   
</template>

<script setup lang="ts">

</script>

<style scoped>
    .main {
        width:100vw;
        min-height: 100vh;
    }
    nav {  
        background-color:rgb(97, 94, 250);
        display:flex;
        width: 100%;
    }
    .opcion_menu{
        margin:0.5em;
        padding:0.5em;
        border-radius: 5px;
        background-color:antiquewhite;
        color: rgb(49, 49, 49);
        display:flex;
    }
    .opcion_menu * {
        padding: 0.2em 0.5em;
    }
    .router-link-active , .router-link-exact-active {
        color: rgb(248, 242, 248);    
        background-color: rgb(49, 49, 49);
    }
</style>
