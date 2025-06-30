import type { Categoria } from '@/interface/Categoria'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

const url = 'categorias/'

const useCategoriasStore = defineStore('categorias', () => {
  const categorias = ref<Array<Categoria>>([])
  const categoria = ref<Categoria>({
    id: 0,
    nombre: ''
  })

  function buscar_categoria(id: number){
    const la_cat = categorias.value.find((cat) => cat.id === id)
    if (la_cat)
      categoria.value = la_cat
    else {
      categoria.value.id = 0
      categoria.value.nombre = ''
    }
    return categoria
  }

  async function getAll(){
     try {
      const respuesta = await ApiService.getAll(url)
      categorias.value = respuesta //Respuesta tiene el listado de categorias
    } catch (error: any) {
      categorias.value = []
      throw error 
    }
  }
  
  async function getOne(id: number){
     try {
      const respuesta = await ApiService.getOne(url, id)
      categoria.value = respuesta //Respuesta tiene la categoria
    } catch (error: any) { 
      throw error
    }
  }
  async function create(una_categoria: Categoria){
    try {
      const respuesta = await ApiService.create(url, una_categoria)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto){
        await getAll()  //para robustez de la app
        categoria.value = respuesta.objeto  //Respuesta.objeto tiene la categoria creada
        return respuesta.objeto 
      }else{
         throw new Error("Error al crear la categoria: Respuesta inesperada del servidor.")
      }
    } catch (error: any) {
      throw error 
    }
  }
  async function update(una_categoria: Categoria){
     if (!una_categoria.id)
       throw new Error("Error: No se puede actualizar una categoria sin ID.")
    try {
      const respuesta = await ApiService.update(url, una_categoria.id, una_categoria)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto){
        await getAll()  //para robustez de la app
        categoria.value = respuesta.objeto  //Respuesta.objeto tiene la marca actualizada
        return respuesta.objeto 
      }else{
        throw new Error("Error al actualizar la categoria: Respuesta inesperada del servidor.")
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

  return {categorias, categoria, buscar_categoria, getAll, getOne, create, update, destroy}

})

export default useCategoriasStore
