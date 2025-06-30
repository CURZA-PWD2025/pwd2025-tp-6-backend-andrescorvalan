const proveedores_routes = [
	{
		path: '/proveedores',
		name: 'proveedores',
		component: () => import('../views/ProveedoresView.vue'),
		children: [
			{
				path: '',
				name: 'proveedores_list',
				component: () => import('../components/Proveedores/ProveedorList.vue')
			},
			{
				path: ':id/show',
				name: 'proveedores_show',
				component: () => import('../components/Proveedores/ProveedorShow.vue')
			},
			{
				path: 'create',
				name: 'proveedores_create',
				component: () => import('../components/Proveedores/ProveedorCreate.vue')
			},
			{
				path: 'update/:id/edit',
				name: 'proveedores_update',
				component: () => import('../components/Proveedores/ProveedorUpdate.vue'),
			},
		]
	}
]
export default proveedores_routes
