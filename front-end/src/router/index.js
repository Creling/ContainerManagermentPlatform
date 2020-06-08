import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/dashboard',
                    component: () => import(/* webpackChunkName: "dashboard" */ '../components/page/Dashboard.vue'),
                    meta: { title: '系统首页' }
                },
                {
                    path: '/table',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/Country.vue'),
                    meta: { title: '国家列表' }
                },
                {
                    path: '/city',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/City.vue'),
                    meta: { title: '城市列表' }
                },
                {
                    path: '/datacenter',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/Datacenter.vue'),
                    meta: { title: '数据中心列表' }
                },
                {
                    path: '/provider',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/Provider.vue'),
                    meta: { title: '提供商列表' }
                },
                {
                    path: '/container',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/Container.vue'),
                    meta: { title: '容器列表' }
                },
                {
                    path: '/service',
                    component: () => import(/* webpackChunkName: "form" */ '../components/page/Service.vue'),
                    meta: { title: '服务列表' }
                },
                {
                    path: '/servicecontainer',
                    component: () => import(/* webpackChunkName: "form" */ '../components/page/ServiceContainer.vue'),
                    meta: { title: '服务部署列表' }
                },
                {
                    path: '/404',
                    component: () => import(/* webpackChunkName: "404" */ '../components/page/404.vue'),
                    meta: { title: '404' }
                },
                {
                    path: '/403',
                    component: () => import(/* webpackChunkName: "403" */ '../components/page/403.vue'),
                    meta: { title: '403' }
                }
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue')
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});
