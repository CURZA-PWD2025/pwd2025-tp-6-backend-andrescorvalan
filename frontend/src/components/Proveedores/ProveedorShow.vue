<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useProveedoresStore from '../../stores/proveedores_store'
  import axios from 'axios'; //para manejar error
  import { useRoute } from 'vue-router';
  
  const route = useRoute()

  const { proveedor } = toRefs(useProveedoresStore())
  const { buscar_proveedor } = useProveedoresStore()
  
  onMounted(() => {
    let id: number
    if (Array.isArray(route.params.id)) 
      id = parseInt(route.params.id[0])
    else
      id = parseInt(route.params.id);
    buscar_proveedor(id)
    if (proveedor.value.id==0)
      alert('No existe el proveedor')
  })
</script>

<template>
  <main>
    <h1>Detalles de la Marca</h1>
    <div class="proveedor">

    <p>Id: {{proveedor.id}}</p>
    <p>Nombre: {{proveedor.nombre}}</p>
    <p>Telefono: {{proveedor.telefono}}</p>
    <p>Direccon: {{proveedor.direccion}}</p>
    <p>Email: {{proveedor.email}}</p>

    <router-link :to="{name: 'proveedores_list'}">Volver</router-link>
    </div>
  </main>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
} 
.proveedor {
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