import request from '../utils/request';

export const fetchData = (query) => {
    return request({
        url: '/api/server',
        method: 'post'
    })
}