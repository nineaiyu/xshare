import request from '@/utils/request'

export function login(data) {
    return request({
        url: '/login',
        method: 'post',
        data
    })
}

export function getToken(params) {
    return request({
        url: '/login',
        method: 'get',
        params
    })
}


export function getUserInfo() {
    return request({
        url: '/userinfo',
        method: 'get',
    })
}

export function updateUserInfo(data) {
    return request({
        url: '/userinfo',
        method: 'put',
        data
    })
}

export function logout(data) {
    return request({
        url: '/logout',
        method: 'post',
        data
    })
}

export function refreshToken(data) {
    return request({
        url: '/refresh',
        method: 'post',
        data
    })
}
