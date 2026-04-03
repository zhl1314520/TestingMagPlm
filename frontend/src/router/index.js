import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../Login/LoginPage.vue'
import ForgotPassword from '../Login/ForgotPassword.vue'
import ResetPassword from '../Login/ResetPassword.vue'
import ResetPasswordSuccess from '../Login/ResetPasswordSuccess.vue'
import DashboardLayout from '../Dashboard/DashboardLayout.vue'
import Overview from '../Dashboard/Overview.vue'
import Projects from '../Dashboard/Projects.vue'
import TestCases from '../Dashboard/TestCases.vue'
import Executions from '../Dashboard/Executions.vue'
import Bugs from '../Dashboard/Bugs.vue'
import Reports from '../Dashboard/Reports.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: ResetPassword
  },
  {
    path: '/reset-password-success',
    name: 'ResetPasswordSuccess',
    component: ResetPasswordSuccess
  },
  {
    path: '/dashboard',
    component: DashboardLayout,
    children: [
      {
        path: '',
        name: 'Overview',
        component: Overview
      },
      {
        path: 'projects',
        name: 'Projects',
        component: Projects
      },
      {
        path: 'testcases',
        name: 'TestCases',
        component: TestCases
      },
      {
        path: 'executions',
        name: 'Executions',
        component: Executions
      },
      {
        path: 'bugs',
        name: 'Bugs',
        component: Bugs
      },
      {
        path: 'reports',
        name: 'Reports',
        component: Reports
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token')
  
  // 公开访问的页面（不需要登录）
  const publicPages = ['/login', '/forgot-password', '/reset-password', '/reset-password-success']
  
  // 如果访问的是公开页面，直接放行
  if (publicPages.includes(to.path)) {
    // 如果已登录且访问登录页，跳转到 dashboard
    if (to.path === '/login' && token) {
      next('/dashboard')
    } else {
      next()
    }
  } else {
    // 访问需要登录的页面
    if (!token) {
      next('/login')
    } else {
      next()
    }
  }
})

export default router
