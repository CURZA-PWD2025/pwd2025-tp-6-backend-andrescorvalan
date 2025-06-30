<script setup lang="ts">
  import { toRefs, onMounted, ref } from 'vue';
  import axios from 'axios'; //para manejar error
 
  import { useRoute } from 'vue-router';

  import useMarcasStore from '../../stores/marcas_store'
  import useProveedoresStore from '../../stores/proveedores_store'
  import useArticulosStore from '../../stores/articulos_store';
  import useCategoriasStore from '../../stores/categorias_store';
    
  const route = useRoute()
  
  const { articulo } = toRefs(useArticulosStore())
  const { update, getAll, buscar_articulo } = useArticulosStore()

  const { marcas } = toRefs(useMarcasStore())
  const { buscar_marca, getAll:getAllMarcas } = useMarcasStore()
  const { proveedores } = toRefs(useProveedoresStore())
  const { buscar_proveedor, getAll:getAllProveedores } = useProveedoresStore()
  const { categorias } = toRefs(useCategoriasStore())
  const { buscar_categoria, getAll:getAllCategorias } = useCategoriasStore()

  const categorias_select_id = ref<number[]>([])

  onMounted(async () => {
    let id: number
    if (Array.isArray(route.params.id)) 
      id = parseInt(route.params.id[0])
    else
      id = parseInt(route.params.id);
    buscar_articulo(id)
    if (articulo.value.id==0)
      alert('No existe el articulo')
    else{
      categorias_select_id.value=[]
      articulo.value.categorias.forEach(element => {
        if(element.id)
          categorias_select_id.value.push(element.id)
      })
      await getAllMarcas()
      await getAllProveedores()
      await getAllCategorias()
    }
  })

  async function modificar_articulo(){
    if(!articulo.value.descripcion || !articulo.value.marca.id || !articulo.value.proveedor.id)
      alert("Debe completar campos: descripcion, marca y proveedor")
    else{
      try {
        articulo.value.marca = buscar_marca(articulo.value.marca.id).value
        articulo.value.proveedor = buscar_proveedor(articulo.value.proveedor.id).value
        let error = 0
        articulo.value.categorias=[]
        categorias_select_id.value.forEach(element => {
          const una_categoria = buscar_categoria(element)
          if(una_categoria.value.id)
            articulo.value.categorias.push(una_categoria.value)
          else
            error = 1
        })
        if(articulo.value.marca.id && articulo.value.proveedor.id && !error){
          await update(articulo.value)
          await getAll()
          alert("Articulo modificado correctamente")
        }else{
          alert("Error, algun dato ya no existe en el store. Se anula la creacion")
        }
      } catch (error: any) {
        console.error("Error al modificar articulo:", error);
        let mensaje = "Ocurrió un error al modificar el articulo. Intente nuevamente.";
        if (axios.isAxiosError(error)) {
          if (error.response) {
            if (error.response.data && error.response.data.mensaje)
              mensaje = `Error: ${error.response.data.mensaje}`;
            else
               mensaje = `Error del servidor (Código: ${error.response.status}).`
          }else
            mensaje = "No se pudo conectar al servidor. Verifique su conexión e intente nuevamente." 
        }else
          mensaje = 'Ocurrió un error inesperado';
        alert(mensaje)
      }
    }
  } 
</script>

<template>
  <main>
  <h1>Modificar un Articulo</h1>
  <div class="articulo">
    <h1>Datos del Articulo</h1>
    <form @submit.prevent="modificar_articulo" class="formulario">
      <label class="labelField">Descripcion:
        <abbr title="Ingrese la descripcion del articulo (obligatorio)">*</abbr>
        <input type="text" v-model="articulo.descripcion" placeholder="Debe ingresar una descripcion para el articulo" maxlength="50" pattern="[A-Za-z0-9 ]*" required>
      </label>
      <label class="labelField">Precio:
        <abbr title="Ingrese la descripcion del articulo (obligatorio)">*</abbr>
        <input type="text" v-model="articulo.precio" placeholder="Debe ingresar el precio del articulo" pattern="^\d+(\.\d{1,2})?$">
      </label>
      <label class="labelField">Stock:
        <abbr title="Ingrese el stock del articulo (obligatorio)">*</abbr>
        <input type="text" v-model="articulo.stock" placeholder="Debe ingresar el stock del articulo" pattern="^\d+$">
      </label>
      <label class="labelField">Marca:
        <abbr title="Ingrese la marca del articulo (obligatorio)">*</abbr>
        <div class="select">
          <fieldset v-for="marca_aux in marcas" :key="marca_aux.id">
            <label :for="'marca-'+marca_aux.id">{{ marca_aux.nombre }} 
            <input type="radio" :id="'marca-'+marca_aux.id"  v-model="articulo.marca.id" name="la_marca" :value="marca_aux.id">
            </label>
          </fieldset>
        </div>
      </label>
      <label class="labelField">Proveedor:
        <div class="select">
          <fieldset v-for="proveedor_aux in proveedores" :key="proveedor_aux.id">
            <label :for="'proveedor-'+proveedor_aux.id">{{ proveedor_aux.nombre }} 
            <input type="radio" :id="'proveedor-'+proveedor_aux.id"  v-model="articulo.proveedor.id" name="el_proveedor" :value="proveedor_aux.id">
            </label>
          </fieldset>
        </div>
      </label>
      categorias
       <!-- <label class="labelField">Categorias: -->
        <div class="select">
          <div v-for="categorias_aux in categorias" :key="categorias_aux.id">
            <label :for="'categoria-'+categorias_aux.id">{{ categorias_aux.nombre }}  </label>
            <input type="checkbox" :id="'categoria-'+categorias_aux.id" :value="categorias_aux.id" v-model="categorias_select_id" name="las_categorias" >
           
          </div>
        </div>
      <!-- </label> -->

      <fieldset>
        <input type="submit" class="boton" value="Modificar Articulo">
        <input type="reset" class="boton" value="Limpiar Campo">
      </fieldset>
    </form>
  </div>
  </main>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
} 
.articulo {
  margin:0.5em;
  text-align: center;
}
.formulario {
  background-color:gainsboro;
  border-radius: 0.5em 0.5em 0.5em 0.5em;
  border: 1px solid blue;
  margin: 0.5em;
  text-align: left;
}
.select {
  text-align: center;
  display: flex;
}

fieldset {
  border: 0;
  margin: 0.5em;
  text-align: center;
}
.labelField {
  display: block;
  margin: 0.5em;
}
.labelField abbr {
  display: inline-block;
  color: red;
  text-decoration: none;
}
input {
  border-radius: 0.5em 0.5em 0.5em 0.5em;
  border: 1px solid green;
  width: 100%;
  height:2em;
}
.boton{
  border-radius: 0.5em 0.5em 0.5em 0.5em;
  border: 1px solid blue;
  display: inline-block;
  margin: 0.5em;
  padding: 0.2em 0.4em 0.2em 0.4em;
  text-align: right;
  width: auto;
}
h1 {
  margin:0.5em;
  text-align: left;
  font-size: 3em;
  font-family:Georgia, 'Times New Roman', Times, serif;
}
</style>