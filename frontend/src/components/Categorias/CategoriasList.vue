<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useCategoriasStore from '../../stores/categorias_store'
  import { RouterLink } from 'vue-router';

  const {categorias} = toRefs(useCategoriasStore())
  const {getAll, destroy} = useCategoriasStore()
  
  onMounted(async () => {
    await getAll()
  })

  async function eliminar(id: number){
    if (confirm('Desea eliminar la Categorias')){
      await destroy(id)
      await getAll()
    }
  }
</script>

<template>
  <main>
    <h1>Listado de Categorias</h1>
    <div class="listado">
        <article class="registro" v-for="categoria in categorias" :key="categoria.id">
          <h2>Id: {{ categoria.id }}</h2>
          <h2>Nombre {{ categoria.nombre}}</h2>
          <router-link :to="{name:'categorias_show', params:{id: categoria.id }}"><button>Mostrar</button></router-link>
          <router-link :to="{name:'categorias_update', params: {id: categoria.id}}"><button>Editar</button></router-link>
          <button @click.prevent="eliminar(categoria.id as number)">Eliminar</button>
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
      text-align: center;
      width: 20em;
      border: 2px solid blue;
      border-radius: 10px;
      background-color: white;
  }
</style>