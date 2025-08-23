// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

// 导入组件
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import ArticleEditor from '../views/ArticleEditor.vue'
import ArticleDetail from '../views/ArticleDetail.vue'
import RoadmapEditor from '../views/RoadmapEditor.vue'
import MindmapEditor from '../views/MindmapEditor.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/article/new',
    name: 'NewArticle',
    component: ArticleEditor,
    meta: { requiresAuth: true }
  },
  {
    path: '/article/:id/edit',
    name: 'EditArticle',
    component: ArticleEditor,
    meta: { requiresAuth: true }
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: ArticleDetail,
    meta: { requiresAuth: false }
  },
  {
    path: '/roadmap/new',
    name: 'NewRoadmap',
    component: RoadmapEditor,
    meta: { requiresAuth: true }
  },
  {
    path: '/roadmap/:id/edit',
    name: 'EditRoadmap',
    component: RoadmapEditor,
    meta: { requiresAuth: true }
  },
  {
    path: '/mindmap/new',
    name: 'NewMindmap',
    component: MindmapEditor,
    meta: { requiresAuth: true }
  },
  {
    path: '/mindmap/:id/edit',
    name: 'EditMindmap',
    component: MindmapEditor,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  
  // 管理员路由
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/AdminLogin.vue'),
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/admin/register',
    name: 'AdminRegister',
    component: () => import('../views/AdminRegister.vue'),
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 初始化认证状态（仅在首次访问时）
  if (!authStore.isAuthenticated && localStorage.getItem('auth_token')) {
    await authStore.initAuth()
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // 如果是管理员页面，重定向到管理员登录
    if (to.path.startsWith('/admin/')) {
      next('/admin/login')
    } else {
      next('/login')
    }
    return
  }
  
  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin && (!authStore.currentUser || !authStore.currentUser.is_admin)) {
    next('/admin/login')
    return
  }
  
  // 已登录用户访问登录/注册页面时重定向
  if (to.meta.hideForAuth && authStore.isLoggedIn) {
    // 如果是管理员，重定向到管理员仪表板
    if (authStore.currentUser && authStore.currentUser.is_admin && to.path.startsWith('/admin/')) {
      next('/admin/dashboard')
    } else {
      next('/dashboard')
    }
    return
  }
  
  next()
})

export default router

