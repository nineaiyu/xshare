import request from '@/utils/request'


export function getFileShare(params) {
    return request({
        url: '/short',
        method: 'get',
        params: params
    })
}

export function getFileUrl(data) {
    return request({
        url: '/short',
        method: 'post',
        data
    })
}
