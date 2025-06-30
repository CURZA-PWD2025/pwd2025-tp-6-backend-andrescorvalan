<script setup lang="ts">
  import { toRefs, onMounted } from 'vue';
  import useProveedoresStore from '../../stores/proveedores_store'
  import axios from 'axios'; //para manejar error

  const { proveedor } = toRefs(useProveedoresStore())
  const { create } = useProveedoresStore()


  onMounted(() => {
    proveedor.value.nombre=''
    proveedor.value.telefono=''
    proveedor.value.direccion=''
    proveedor.value.email=''
  })

  async function nueva_proveedor(){
     if(!proveedor.value.nombre || !proveedor.value.telefono ||  !proveedor.value.direccion || !proveedor.value.email)
      alert("Debe completar todos los campos")
    else{
      try {
        await create(proveedor.value)
        alert("Proveedor creado correctamente")
        proveedor.value.nombre=''
        proveedor.value.telefono=''
        proveedor.value.direccion=''
        proveedor.value.email=''
      } catch (error: any) {
        console.error("Error al crear el proveedor:", error);
        let mensaje = "Ocurrió un error al crear el proveedor. Intente nuevamente.";
        
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
        proveedor.value.nombre=''
        proveedor.value.telefono=''
        proveedor.value.direccion=''
        proveedor.value.email=''
    }
  } 
</script>

<template>
  <main>
    <h1>Crear una Proveedor</h1>
    <div class="categoria">
    <h1>Datos del Proveedor</h1>
      <form @submit.prevent="nueva_proveedor" class="formulario">
      <label class="labelField">Nombre:
        <abbr title="Ingrese el nombre del proveedor (obligatorio)">*</abbr>
        <input type="text" v-model="proveedor.nombre" placeholder="Debe ingresar el nombre del proveedor" maxlength="50" pattern="[A-Za-z ]*" required>
      </label>
      <label class="labelField">Telefono:
        <abbr title="Ingrese el telefono del proveedora (obligatorio)">*</abbr>
        <input type="tel" v-model="proveedor.telefono" placeholder="Debe ingresar el telefono del proveedor" maxlength="50" pattern="[0-9 ]*" required>
      </label>
      <label class="labelField">Direccion:
        <abbr title="Ingrese la direccion de la categoria (obligatorio)">*</abbr>
        <input type="text" v-model="proveedor.direccion" placeholder="Debe ingresar la direccion del proveedor" maxlength="50" pattern="[A-Za-z0-9 ]*" required>
      </label>
      <label class="labelField">Correo electronico:
        <abbr title="Déjenos un email para contactarlo (usuario@dominio) (obligatorio)">*</abbr>
        <input type="email" v-model="proveedor.email" placeholder="Debe ingresar el email del proveedor" required>
      </label>

      <fieldset>
        <input type="submit" class="boton" value="Crear Proveedor">
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
.proveedor {
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