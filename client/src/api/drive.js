import request from '@/utils/request'

export function login(data) {
    return request({
        url: '/login',
        method: 'post',
        data
    })
}

export function getQrDrive() {
    return request({
        url: '/qrdrive',
        method: 'get',
    })
}

export function checkQrDrive(data) {
    return request({
        url: '/qrdrive',
        method: 'post',
        data
    })
}


export function getDrive(params) {
    return request({
        url: '/drive',
        method: 'get',
        params: params
    })
}

export function delDrive(id) {
    return request({
        url: '/drive/' + id,
        method: 'delete',
    })
}

export function operateDrive(data) {
    return request({
        url: '/drive',
        method: 'post',
        data
    })
}

export function updateDrive(params) {
    return request({
        url: '/drive/' + params.id,
        method: 'put',
        data: params
    })
}
