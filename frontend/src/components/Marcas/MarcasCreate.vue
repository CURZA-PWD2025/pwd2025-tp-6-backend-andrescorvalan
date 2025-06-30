<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useMarcasStore from '../../stores/marcas_store'
  import axios from 'axios'; //para manejar error

  const { marca } = toRefs(useMarcasStore())
  const { create } = useMarcasStore()

  onMounted(() => {
    marca.value.nombre=''
  })

  async function nueva_marca(){
     if(!marca.value.nombre)
      alert("Debe completar todos los campos")
    else{
      try {
        await create(marca.value)

        alert("Marca creada correctamente")
        marca.value.nombre=''
      } catch (error: any) {
        console.error("Error al crear marca:", error);
        let mensaje = "Ocurrió un error al crear la marca. Intente nuevamente.";
        
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
    <h1>Crear una Marca</h1>
    <div class="marca">
    <h1>Datos de la Marca</h1>
      <form @submit.prevent="nueva_marca" class="formulario">
      <label class="labelField">Nombre:
        <abbr title="Ingrese el nombre de la marca (obligatorio)">*</abbr>
        <input type="text" v-model="marca.nombre"  placeholder="Debe ingresar el nombre de la marca" maxlength="50" pattern="[A-Za-z0-9 ]*" required>
      </label>
      <fieldset>
        <input type="submit" class="boton" value="Crear Marca">
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
.marca {
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