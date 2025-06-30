<template>
  <h1>Administración de Articulos</h1>
  <router-link :to="{name: 'articulos_create'}">Crear un nuevo articulo</router-link>
  <router-view/>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

import { onMounted } from 'vue';

const route = useRouter()

onMounted(() => {
  route.push({name: 'articulos_list'})
})

</script>

<style scoped>

</style>