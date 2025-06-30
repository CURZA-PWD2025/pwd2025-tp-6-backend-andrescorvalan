const marcas_routes = [
	{
		path: '/marcas',
		name: 'marcas',
		component: () => import('../views/MarcasView.vue'),
		children: [
			{
				path: '',
				name: 'marcas_list',				
				component: () => import('../components/Marcas/MarcasList.vue')
			},
			{
				path: ':id/show',
				name: 'marcas_show',
				component: () => import('../components/Marcas/MarcasShow.vue')
			},
			{
				path: 'create',
				name: 'marcas_create',
				component: () => import('../components/Marcas/MarcasCreate.vue'),
			},
			{
				path: 'update/:id/edit',
				name: 'marcas_update',
				component: () => import('../components/Marcas/MarcasUpdate.vue'),
			},
		]
	}
]
export default marcas_routes
