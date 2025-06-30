const categorias_routes = [
	{
		path: '/categorias',
		name: 'categorias',
		component: () => import('../views/CategoriasView.vue'),
		children: [
			{
				path: '',
				name: 'categorias_list',
				component: () => import('../components/Categorias/CategoriasList.vue')
			},
			{
				path: ':id/show',
				name: 'categorias_show',
				component: () => import('../components/Categorias/CategoriasShow.vue')
			},
			{
				path: 'create',
				name: 'categorias_create',
				component: () => import('../components/Categorias/CategoriasCreate.vue'),
			},
			{
				path: 'update/:id/edit',
				name: 'categorias_update',
				component: () => import('../components/Categorias/CategoriasUpdate.vue'),
			},
		]
	}
]
export default categorias_routes
