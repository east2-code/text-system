import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import LicenseList from '../views/LicenseList.vue'
import SoftwareList from '../views/SoftwareList.vue'
import OperationLog from '../views/OperationLog.vue'
import Settings from '../views/Settings.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/licenses', name: 'LicenseList', component: LicenseList, meta: { requiresAuth: true } },
  { path: '/software', name: 'SoftwareList', component: SoftwareList, meta: { requiresAuth: true } },
  { path: '/logs', name: 'OperationLog', component: OperationLog, meta: { requiresAuth: true } },
  { path: '/settings', name: 'Settings', component: Settings, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path === '/login') {
    if (token) return next('/')
    return next()
  }
  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }
  next()
})

export default router