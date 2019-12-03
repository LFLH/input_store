import Vue from 'vue'
import Router from 'vue-router'
import add from '@/components/add'
import all from '@/components/all'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'add',
      component: add
    },
    {
      path: '/all',
      name: 'all',
      component: all
    }
  ]
})
