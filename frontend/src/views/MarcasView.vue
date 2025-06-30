<template>
  <h1>Administración de Marcas</h1>
  <router-link :to="{name: 'marcas_create'}">Crear una nueva Marca</router-link>
  <router-view/>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

import { onMounted } from 'vue';

const route = useRouter()

onMounted(() => {
  route.push({name: 'marcas_list'})
})

</script>

<style scoped>

</style>

