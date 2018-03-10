import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Dev from '@/components/Dev'

Vue.use Router

export default new Router(
  routes: [
    {
      path: '/'
      name: 'Home'
      component: Home
    }
    {
      path: '/dev'
      name: 'Dev'
      component: Dev
    }
  ]
)
