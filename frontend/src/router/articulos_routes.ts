const articulos_routes = [
	{
		path: '/articulos',
		name: 'articulos',
		component: () => import('../views/ArticulosView.vue'),
		children: [
			{
				path: '',
				name: 'articulos_list',				
				component: () => import('../components/Articulos/ArticulosList.vue'),
			},
			{
				path: ':id/show',
				name: 'articulos_show',
				component: () => import('../components/Articulos/ArticulosShow.vue'),
			},
			{
				path: 'create',
				name: 'articulos_create',
				component: () => import('../components/Articulos/ArticulosCreate.vue'),
			},
			{
				path: 'update/:id/edit',
				name: 'articulos_update',
				component: () => import('../components/Articulos/ArticulosUpdate.vue'),
			},
		]
	}
]
export default articulos_routes
