import type { Marca } from "./Marca"
import type { Proveedor } from "./Proveedor"
import type { Categoria } from "./Categoria"

export interface Articulo{
  id?: number,
  descripcion: string,
  precio: number,
  stock: number,
  marca: Marca,
  proveedor: Proveedor,
  categorias: Array<Categoria>
}