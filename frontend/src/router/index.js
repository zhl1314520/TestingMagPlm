import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../Login/LoginPage.vue'
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
  
  if (to.path !== '/login' && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
