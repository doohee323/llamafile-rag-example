import Vue from 'vue'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap/dist/js/bootstrap.js'

import '@/assets/_shared.scss'

import App from "@/App.vue";
import VueRouter from 'vue-router'
import routes from '@/router'

Vue.use(VueRouter);

const router = new VueRouter({
    routes: routes,
    mode: 'history'
})

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Vue.config.productionTip = false

new Vue({
    router,
    render: h => h(App)
}).$mount('#app');
