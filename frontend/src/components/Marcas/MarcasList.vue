<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useMarcasStore from '../../stores/marcas_store'
  import { RouterLink } from 'vue-router';

  const {marcas} = toRefs(useMarcasStore())
  const {getAll, destroy} = useMarcasStore()
  
  onMounted(async () => {
    console.log('montando y leyendo base de datos')
    await getAll()
  })

  async function eliminar(id: number){
    if (confirm('Desea eliminar la Marca')){
      await destroy(id)
      await getAll()
    }
  }
</script>

<template>
  <main>
    <h1>Listado de Marcas</h1>
    <div class="listado">
        <article class="registro" v-for="marca in marcas" :key="marca.id">
           <!-- {{ console.log('Objeto marca en v-for:', marca) }} 
          {{ marca.nombre }} -->
          <h2>Id: {{ marca.id }} </h2>
          <h2>Nombre: {{ marca.nombre }}</h2>
          <router-link :to="{name:'marcas_show', params:{id: marca.id }}"><button>Mostrar</button></router-link>
          <router-link :to="{name:'marcas_update', params: {id: marca.id}}"><button>Editar</button></router-link>
         <button @click.prevent="eliminar(marca.id as number)">Eliminar</button>
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