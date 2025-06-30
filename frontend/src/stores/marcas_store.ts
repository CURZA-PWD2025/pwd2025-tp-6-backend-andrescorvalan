import type { Marca } from '@/interface/Marca'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

const url = 'marcas/'

const useMarcasStore = defineStore('marcas', () => {
  const marcas = ref<Array<Marca>>([])
  const marca = ref<Marca>({
    id: 0,
    nombre: ''
  })
  
  function buscar_marca(id: number){
    const la_marca = marcas.value.find((marca) => marca.id === id)
    if (la_marca)
      marca.value = la_marca
    else {
      marca.value.id = 0
      marca.value.nombre = ''
    }
    return marca
  }

  async function getAll(){
    try {
      const respuesta = await ApiService.getAll(url)
      marcas.value = respuesta //Respuesta tiene el listado de marcas
    } catch (error: any) {
      marcas.value = []
      throw error 
    }
  }
  
  async function getOne(id: number){
    try {
      const respuesta = await ApiService.getOne(url, id)
      marca.value = respuesta //Respuesta tiene la marcas
    } catch (error: any) { 
      throw error
    }
  }
  
  async function create(una_marca: Marca){
    try {
      const respuesta = await ApiService.create(url, una_marca)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto){
        await getAll()  //para robustez de la app
        marca.value = respuesta.objeto  //Respuesta.objeto tiene la marca creada
        return respuesta.objeto 
      }else{
         throw new Error("Error al crear marca: Respuesta inesperada del servidor.")
      }
    } catch (error: any) {
      throw error 
    }
  }
  
  async function update(una_marca: Marca){
    if (!una_marca.id)
       throw new Error("Error: No se puede actualizar una marca sin ID.")
    try {
      const respuesta = await ApiService.update(url, una_marca.id, una_marca)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto){
        await getAll()  //para robustez de la app
        marca.value = respuesta.objeto  //Respuesta.objeto tiene la marca actualizada
        return respuesta.objeto 
      }else{
        throw new Error("Error al actualizar marca: Respuesta inesperada del servidor.")
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

  return {marcas, marca, buscar_marca, getAll, getOne, create, update, destroy}

})

export default useMarcasStore
