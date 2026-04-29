import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../views/ChatView.vue'
import LoginView from '../views/LoginView.vue'
import GroupView from '../views/GroupView.vue'
import AdminPanel from '../views/AdminPanel.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/chatflow',
      name: 'chatflow',
      component: ChatView,
      meta: { requiresAuth: true }
    },
    {
      path: '/group',
      name: 'group',
      component: GroupView,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPanel,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/login',
      name: 'login-page',
      component: LoginView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('userToken')
  const userInfoStr = localStorage.getItem('userInfo')
  const userInfo = userInfoStr ? JSON.parse(userInfoStr) : null
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAdmin && (!userInfo || userInfo.role !== 'admin')) {
    next('/group')
  } else if (to.path === '/login' && token) {
    next('/chatflow')
  } else {
    next()
  }
})

export default router