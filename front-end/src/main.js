import Vue from 'vue';
import App from './App.vue';
import router from './router';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
import './assets/css/icon.css';
import './components/common/directives';
import 'babel-polyfill';
import VueMeta from 'vue-meta'

Vue.config.productionTip = false;
Vue.use(ElementUI, {
    size: 'small'
});
Vue.use(VueMeta, {
    // optional pluginOptions
    refreshOnceOnNavigation: true
  });

//使用钩子函数对路由进行权限跳转
router.beforeEach((to, from, next) => {

    document.title = `容器管理平台`;
    
    const role = localStorage.getItem('ms_username');
    if (!role && to.path !== '/login') {
        next('/login');
    } else {
        next();
    }

    
});

new Vue({
    router,
    render: h => h(App)
}).$mount('#app');