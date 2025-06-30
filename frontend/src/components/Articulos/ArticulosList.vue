<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useArticulosStore from '../../stores/articulos_store'
  import { RouterLink } from 'vue-router';

  const {articulos} = toRefs(useArticulosStore())
  const {getAll, destroy} = useArticulosStore()
  
  onMounted(async () => {
      await getAll()
  })

  async function eliminar(id: number){
    if (confirm('Desea eliminar el articulo')){
      await destroy(id)
      await getAll()
    }
  }
</script>

<template>
  <main>
    <h1>Listado de Articulos</h1>
    <div class="listado">
        <article class="registro" v-for="articulo in articulos" :key="articulo.id">
          <h2>Id: {{ articulo.id }} </h2>
          <h2>Descripcion: {{ articulo.descripcion }} </h2>
          <h2>Precio: {{ articulo.precio }} </h2>
          <h2>Stock: {{ articulo.stock }} </h2>
          <h2>Marca: {{ articulo.marca.nombre }} </h2>
          <h2>Proveedor: {{ articulo.proveedor.nombre }} </h2>
          <h2>Categorias: {{ articulo.categorias.length }} catergoria/s</h2>
          <router-link :to="{name:'articulos_show', params:{id: articulo.id }}"><button>Mostrar</button></router-link>
          <router-link :to="{name:'articulos_update', params: {id: articulo.id}}"><button>Editar</button></router-link>
         <button @click.prevent="eliminar(articulo.id as number)">Eliminar</button>
        </article>
    </div>
  </main>
</template>

<style scoped>
  .listado {
        display: flex;
        flex-wrap: wrap;
        place-items: bottom;
        justify-content: center;
        margin: 2em;
  }
  .registro {
      margin: 0.5em;
      padding: 0.5em;
      text-align: left;
      width: 40em;
      border: 2px solid blue;
      border-radius: 10px;
      background-color: white;
  }
</style>