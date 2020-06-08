import axios from 'axios';
import qs from 'qs';

const service = axios.create({
    // process.env.NODE_ENV === 'development' 来判断是否开发环境
    withCredentials: true,
    baseURL: '//127.0.0.1:8081',
    timeout: 5000
})

service.interceptors.request.use( config => {
    /*
    if(config.method  === 'put'){
        config.data = qs.stringify(config.data);
    }
    */
    return config;
}, error => {
    console.log(error);
    return Promise.reject();
})

service.interceptors.response.use(response => {
    return response.data;
}, error => {
    return Promise.reject(error.response);
})

export  default service;