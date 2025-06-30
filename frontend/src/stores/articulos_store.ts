import type { Articulo } from '@/interface/Articulo'
import type { Marca } from '@/interface/Marca'
import type { Proveedor } from '@/interface/Proveedor'
import type { Categoria } from '@/interface/Categoria'


import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

const url = 'articulos/'

const useArticulosStore = defineStore('articulos', () => {
  const articulos = ref<Array<Articulo>>([])
  const articulo = ref<Articulo>({
    id: 0,
    descripcion: '',
    precio: 0,
    stock: 0,
    marca: {id: 0, nombre: ''},
    proveedor: { id: 0, nombre: '', direccion: '', telefono: '', email: ''},
    categorias: []
  })

  function buscar_articulo(id: number){
    const el_art = articulos.value.find((art) => art.id === id)
    if (el_art)
      articulo.value = el_art
    else {
      articulo.value.id = 0
      articulo.value.descripcion = ''
      articulo.value.precio = 0
      articulo.value.stock = 0
      articulo.value.marca= {id: 0, nombre: ''}
      articulo.value.proveedor = { id: 0, nombre: '', direccion: '', telefono: '', email: ''}
      articulo.value.categorias = []
    }
    return articulo
  }

  async function getAll(){
     try {
      const respuesta = await ApiService.getAll(url)
      console.log(respuesta)
      articulos.value = respuesta //Respuesta tiene el listado de articulos
    } catch (error: any) {
      articulos.value = []
      throw error 
    }
  }
  
  async function getOne(id: number){
     try {
      const respuesta = await ApiService.getOne(url, id)
      articulo.value = respuesta //Respuesta tiene el articulo
    } catch (error: any) { 
      throw error
    }
  }
  async function create(un_articulo: Articulo){
    try {
      const respuesta = await ApiService.create(url, un_articulo)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto){
        await getAll()  //para robustez de la app
        articulo.value = respuesta.objeto  //Respuesta.objeto tiene el articulo creado
        return respuesta.objeto 
      }else{
         throw new Error("Error al crear el articulo: Respuesta inesperada del servidor.")
      }
    } catch (error: any) {
      throw error 
    }
  }
  async function update(un_articulo: Articulo){
     if (!un_articulo.id)
       throw new Error("Error: No se puede actualizar el articulo sin ID.")
    try {
      const respuesta = await ApiService.update(url, un_articulo.id, un_articulo)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto){
        await getAll()  //para robustez de la app
        articulo.value = respuesta.objeto  //Respuesta.objeto tiene el articulo actualizado
        return respuesta.objeto 
      }else{
        throw new Error("Error al actualizar el articulo: Respuesta inesperada del servidor.")
      }
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number){
    try {
      const respuesta = await ApiService.destroy(url, id)
      await getAll() 
      return true
    } catch (error: any) {
      throw error
    }
  }

  return {articulos, articulo, buscar_articulo, getAll, getOne, create, update, destroy}

})

export default useArticulosStore
