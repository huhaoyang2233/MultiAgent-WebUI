import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../views/ChatView.vue'
import LoginView from '../views/LoginView.vue'
import GroupView from '../views/GroupView.vue'

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
      path: '/login',
      name: 'login-page',
      component: LoginView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('userToken')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/chatflow')
  } else {
    next()
  }
})

export default router