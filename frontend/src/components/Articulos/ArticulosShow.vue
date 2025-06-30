<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useArticulosStore from '../../stores/articulos_store'
  import axios from 'axios'; //para manejar error
  import { useRoute } from 'vue-router';
  
  const route = useRoute()

  const { articulo } = toRefs(useArticulosStore())
  const { buscar_articulo } = useArticulosStore()

  onMounted(() => {
    let id: number
    if (Array.isArray(route.params.id)) 
      id = parseInt(route.params.id[0])
    else
      id = parseInt(route.params.id);
    buscar_articulo(id)
    if (articulo.value.id==0)
      alert('No existe el articulo')
  })
</script>

<template>
  <main>
    <h1>Detalles del Articulo</h1>
    <div class="marca">
          <h2>Id: {{ articulo.id }} </h2>
          <h2>Descripcion: {{ articulo.descripcion }} </h2>
          <h2>Precio: {{ articulo.precio }} </h2>
          <h2>Stock: {{ articulo.stock }} </h2>
          <h2>Marca</h2>
          <h2>-Id: {{ articulo.marca.id }} </h2>
          <h2>-Nombre: {{ articulo.marca.nombre }} </h2>
          <h2>Proveedor</h2>
          <h2>-Id: {{ articulo.proveedor.id }} </h2>
          <h2>-Nombre: {{ articulo.proveedor.nombre }} </h2>
          <h2>-Direccion: {{ articulo.proveedor.direccion }} </h2>
          <h2>-Telefono: {{ articulo.proveedor.telefono }} </h2>
          <h2>-Email: {{ articulo.proveedor.email }} </h2>
          <h2>Categorias</h2>
          <div v-for="cat in articulo.categorias">
            <h2>-Id: {{ cat.id }} </h2>
            <h2>-Nombre: {{ cat.nombre }} </h2>
          </div>
          
    <router-link :to="{name: 'articulos_list'}">Volver</router-link>
    </div>
  </main>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
} 
.articulo {
  margin:0.5em;
  text-align: center;
}
.formulario {
  background-color:gainsboro;
  border-radius: 0.5em 0.5em 0.5em 0.5em;
  border: 1px solid blue;
  margin: 0.5em;
  text-align: left;
}
fieldset {
  border:0;
  margin: 0.5em;
  text-align: center;
}
.labelField {
  display: block;
  margin: 0.5em;
}
.labelField abbr {
  display: inline-block;
  color: red;
  text-decoration: none;
}
input {
  border-radius: 0.5em 0.5em 0.5em 0.5em;
  border: 1px solid green;
  width: 100%;
  height:2em;
}
.boton{
  border-radius: 0.5em 0.5em 0.5em 0.5em;
  border: 1px solid blue;
  display: inline-block;
  margin: 0.5em;
  padding: 0.2em 0.4em 0.2em 0.4em;
  text-align: right;
  width: auto;
}
h1 {
  margin:0.5em;
  text-align: left;
  font-size: 3em;
  font-family:Georgia, 'Times New Roman', Times, serif;
}
</style>