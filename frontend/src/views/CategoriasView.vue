<template>
    <h1>Categorias</h1>
    <router-link :to="{name: 'categorias_create'}">Crear Categoria</router-link>
    <router-view/>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

import { onMounted } from 'vue';

const route = useRouter()

onMounted(() => {
  route.push({name: 'categorias_list'})
})

</script>

<style scoped>

</style>
