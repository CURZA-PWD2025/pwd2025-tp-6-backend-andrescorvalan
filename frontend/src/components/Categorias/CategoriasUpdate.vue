<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useCategoriasStore from '../../stores/categorias_store'
  import axios from 'axios'; //para manejar error
  import { useRoute } from 'vue-router';
  
  const route = useRoute()

  const { categoria } = toRefs(useCategoriasStore())
  const { buscar_categoria, update, getAll } = useCategoriasStore()

  onMounted(() => {
    let id: number
    if (Array.isArray(route.params.id)) 
      id = parseInt(route.params.id[0])
    else
      id = parseInt(route.params.id);
    buscar_categoria(id)
    if (categoria.value.id==0)
      alert('No existe la categoria')
  })

  async function modificar_categoria(){
     if(!categoria.value.nombre)
      alert("Debe completar todos los campos")
    else{
      try {
        if (await update(categoria.value)){
          alert("Categoria modificada correctamente")
          await getAll()
        }
        else
          alert("Hubo algun error que impidio modificar la categoria.")  
      } catch (error: any) {
        console.error("Error al modificar la categoria:", error);
        let mensaje = "Ocurrió un error al modificar la categorias. Intente nuevamente.";
        
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
    <h1>Modificar una Categorias</h1>
    <div class="categoria">
    <h1>Datos de la Marca</h1>
      <form @submit.prevent="modificar_categoria" class="formulario">
      <label class="labelField">Nombre:
        <abbr title="Nombre de la categoria (obligatorio)">*</abbr>
        <input type="text" v-model="categoria.nombre"  placeholder="Debe ingresar el nombre de la categoria" maxlength="50" pattern="[A-Za-z0-9 ]*" required>
      </label>
      <fieldset>
        <input type="submit" class="boton" value="Guardar Categorias">
        <input type="reset" class="boton" value="Limpiar Campo">
    </fieldset>
    </form>
    <router-link :to="{name: 'categorias_list'}">Volver</router-link>
    </div>
  </main>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
} 
.categoria {
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
fieldset {
  border:0;
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