import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'


import marcas_routes from './marcas_routes'
import categorias_routes from './categorias_routes'
import proveedores_routes from './proveedores_routes'
import articulos_routes from './articulos_routes'

const routes = [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    ...marcas_routes,
    ...categorias_routes,
    ...proveedores_routes,
    ...articulos_routes,
  ]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router