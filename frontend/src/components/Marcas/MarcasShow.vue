<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useMarcasStore from '../../stores/marcas_store'
  import axios from 'axios'; //para manejar error
  import { useRoute } from 'vue-router';
  
  const route = useRoute()

  const { marca } = toRefs(useMarcasStore())
  const { buscar_marca } = useMarcasStore()

  onMounted(() => {
    let id: number
    if (Array.isArray(route.params.id)) 
      id = parseInt(route.params.id[0])
    else
      id = parseInt(route.params.id);
    buscar_marca(id)
    if (marca.value.id==0)
      alert('No existe la marca')
  })
</script>

<template>
  <main>
    <h1>Detalles de la Marca</h1>
    <div class="marca">

    <p>Id: {{marca.id}}</p>
    <p>Nombre: {{marca.nombre}}</p>
    <router-link :to="{name: 'marcas_list'}">Volver</router-link>
    </div>
  </main>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
} 
.marca {
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