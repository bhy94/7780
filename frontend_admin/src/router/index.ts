// Composables
import { createRouter, createWebHistory } from 'vue-router'
import Cookies from "js-cookie";

const routes = [
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: () => import('@/layouts/basic/Main.vue'),
  //   children: [
  //     {
  //       path: '',
  //       name: 'Index',
  //       component: () => import('@/views/Products.vue'),
  //     },
  //     {
  //       path: 'login',
  //       name: 'UserLogin',
  //       component: () => import('@/views/UserLogin.vue'),
  //     },
  //   ]
  // },
  {
    path: '/panel/',
    component: () => import('@/layouts/basic/ViewFrame.vue'),
    children: [
      {
        path: '',
        name: 'Panel',
        component: () => import('@/views/Panel.vue'),
      },
      {
        path: 'add-product',
        name: 'AddProduct',
        component: () => import('@/views/AddProduct.vue'),
      },
      {
        path: 'manage-products',
        name: 'ManageProducts',
        component: () => import('@/views/ManageProducts.vue'),
      },
      {
        path: 'manage-orders',
        name: 'ManageOrders',
        component: () => import('@/views/ManageOrders.vue'),
      },
      {
        path: 'order-express',
        name: 'OrderExpress',
        component: () => import('@/views/OrderExpress.vue'),
      },
      {
        path: 'add-vendor',
        name: 'AddVendor',
        component: () => import('@/views/AddVendor.vue'),
      },
      {
        path: 'add-user',
        name: 'AddUser',
        component: () => import('@/views/AddUser.vue'),
      },
      {
        path: 'manage-users',
        name: 'ManageUsers',
        component: () => import('@/views/ManageUsers.vue'),
      },
      {
        path: 'manage-vendors',
        name: 'ManageVendors',
        component: () => import('@/views/ManageVendors.vue'),
      },
    ],
  },
  {
    path: '/panel/login/',
    component: () => import('@/layouts/basic/Login.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  // @ts-ignore
  routes,
})

const login_role = Cookies.get('role')

router.beforeEach((to, from, next) => {
  if (to.path.startsWith('/panel/login')) {
    if (login_role == 'admin' || login_role == 'vendor') {
      next('/panel/')
    } else if (login_role == 'user') {
      Cookies.remove('role')
      Cookies.remove('search_results')
      Cookies.remove('token')
      Cookies.remove('user_id')
      Cookies.remove('user_username')
      Cookies.remove('vendor_id')
      Cookies.remove('vendor_username')
      next()
    } else {
      // 无登录状态
      next()
    }
  } else if (to.path.startsWith('/panel/') || to.path == '/panel') {
    if (login_role == 'admin' || login_role == 'vendor') {
      next()
    } else if (login_role == 'user') {
      
      Cookies.remove('role')
      Cookies.remove('search_results')
      Cookies.remove('token')
      Cookies.remove('user_id')
      Cookies.remove('user_username')
      Cookies.remove('vendor_id')
      Cookies.remove('vendor_username')
      next("/panel/login")
    } else {
      // 无登录状态
      next('/panel/login/')
    }
  } else {
    next()
  }
})

export default router
