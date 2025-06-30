import type { Proveedor } from '@/interface/Proveedor'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

const url = 'proveedores/'

const useProveedoresStore = defineStore('proveedores', () => {
  const proveedores = ref<Array<Proveedor>>([])
  const proveedor = ref<Proveedor>({
    id: 0,
    nombre: '',
    telefono: '',
    direccion: '',
    email: ''
  })


  function buscar_proveedor(id: number){
    const el_prov = proveedores.value.find((prov) => prov.id === id)
    if (el_prov)
      proveedor.value = el_prov
    else {
      proveedor.value.id = 0
      proveedor.value.nombre = ''
      proveedor.value.telefono = '',
      proveedor.value.direccion = '',
      proveedor.value.email = ''
    }
    return proveedor
  }

  async function getAll(){
     try {
      const respuesta = await ApiService.getAll(url)
      proveedores.value = respuesta //Respuesta tiene el listado de proveedores
    } catch (error: any) {
      proveedores.value = []
      throw proveedores 
    }
  }
  
  async function getOne(id: number){
     try {
      const respuesta = await ApiService.getOne(url, id)
      proveedor.value = respuesta //Respuesta tiene el proveedores
    } catch (error: any) {
      throw error
    }
  }

  async function create(un_proveedor: Proveedor){
    try {
      const respuesta = await ApiService.create(url, un_proveedor)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto){
        await getAll()  //para robustez de la app
        proveedor.value = respuesta.objeto  //Respuesta.objeto tiene la proveedor creada
        return respuesta.objeto 
      }else{
         throw new Error("Error al crear el proveedor: Respuesta inesperada del servidor.")
      }
    } catch (error: any) {
      throw error 
    }
  }

  async function update(un_proveedor: Proveedor){
     if (!un_proveedor.id)
       throw new Error("Error: No se puede actualizar un proveedor sin ID.")
    try {
      const respuesta = await ApiService.update(url, un_proveedor.id, un_proveedor)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto){
        await getAll()  //para robustez de la app
        proveedor.value = respuesta.objeto  //Respuesta.objeto tiene el proveedor actualizado
        return respuesta.objeto 
      }else{
        throw new Error("Error al actualizar el proveedor: Respuesta inesperada del servidor.")
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
  
  return {proveedores, proveedor, buscar_proveedor, getAll, getOne, create, update, destroy}

})

export default useProveedoresStore
