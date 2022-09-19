import request from '@/utils/request'

export function getDownloadUrl(id) {
    return request({
        url: '/download/' + id,
        method: 'get',
    })
}

export function getFileDownloadUrl(id) {
    return request({
        url: '/download/' + id,
        method: 'get',
    })
}

