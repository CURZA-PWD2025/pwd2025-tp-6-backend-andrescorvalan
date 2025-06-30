<template>
    <h1>Proveedores</h1>
    <router-link :to="{name: 'proveedores_create'}">Crear Proveedor</router-link>
    <router-view/>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

import { onMounted } from 'vue';

const route = useRouter()

onMounted(() => {
  route.push({name: 'proveedores_list'})
})

</script>

<style scoped>

</style>
