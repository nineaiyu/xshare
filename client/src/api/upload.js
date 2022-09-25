import request from '@/utils/request'

export function checkPreHash(data) {
    return request({
        url: '/upload',
        method: 'post',
        data: {'action': 'pre_hash', 'file_info': data},
        timeout: 3000
    })
}

export function checkContentHash(data) {
    return request({
        url: '/upload',
        method: 'post',
        data: {'action': 'content_hash', 'file_info': data},
        timeout: 3000
    })
}

export function uploadComplete(data) {
    return request({
        url: '/upload',
        method: 'post',
        data: {'action': 'upload_complete', 'file_info': data},
        timeout: 3000
    })
}

export function getUploadSid() {
    return request({
        url: '/upload',
        method: 'get',
    })
}
