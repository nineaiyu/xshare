import request from '@/utils/request'

export function login(data) {
    return request({
        url: '/login',
        method: 'post',
        data
    })
}

export function getUserInfo() {
    return request({
        url: '/userinfo',
        method: 'get',
    })
}

export function logout() {
    return request({
        url: '/user/logout',
        method: 'post'
    })
}

export function refreshToken(data) {
    return request({
        url: '/token/refresh',
        method: 'post',
        data
    })
}
