<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useProveedoresStore from '../../stores/proveedores_store'
  import { RouterLink } from 'vue-router';

  const {proveedores} = toRefs(useProveedoresStore())
  const {getAll, destroy} = useProveedoresStore()
  
  onMounted(async () => {
    await getAll()
  })

  async function eliminar(id: number){
    if (confirm('Desea eliminar el Proveedor')){
      await destroy(id)
      await getAll()
    }
  }
</script>

<template>
  <main>
    <h1>Listado de Proveedores</h1>
    <div class="listado">
        <article class="registro" v-for="proveedor in proveedores" :key="proveedor.id">
          <h2>Id: {{ proveedor.id }}</h2>
          <h2>Nombre: {{ proveedor.nombre}}</h2>
          <h2>Teléfono: {{ proveedor.telefono}}</h2>
          <h2>Drección: {{ proveedor.direccion}}</h2>
          <h2>Emial {{ proveedor.email}}</h2>
          <router-link :to="{name:'proveedores_show', params:{id: proveedor.id }}"><button>Mostrar</button></router-link>
          <router-link :to="{name:'proveedores_update', params: {id: proveedor.id}}"><button>Editar</button></router-link>
          <button @click.prevent="eliminar(proveedor.id as number)">Eliminar</button>
        </article>
    </div>
  </main>
</template>
<style scoped>
  .listado {
        display: flex;
        flex-wrap: wrap;
        place-items: bottom;
        justify-content: left;
        margin: 2em;
  }
  .registro {
      margin: 0.5em;
      padding: 0.5em;
      text-align: center;
      width:max-content;
      border: 2px solid blue;
      border-radius: 10px;
      background-color: white;
  }
</style>
