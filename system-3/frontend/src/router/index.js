import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import MainLayout from '../layouts/MainLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import LicenseList from '../views/LicenseList.vue'
import LicenseDetail from '../views/LicenseDetail.vue'
import SoftwareList from '../views/SoftwareList.vue'

const routes = [
  { path: '/login', component: Login },
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', component: Dashboard },
      { path: 'licenses', component: LicenseList },
      { path: 'licenses/:id', component: LicenseDetail },
      { path: 'software', component: SoftwareList },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：未登录跳转登录
router.beforeEach((to, from, next) => {
  if (to.path === '/login') return next()
  const token = localStorage.getItem('token')
  if (!token) return next('/login')
  next()
})

export default router