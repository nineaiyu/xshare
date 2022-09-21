import request from '@/utils/request'


export function getFileShare(params) {
    return request({
        url: '/short',
        method: 'get',
        params: params
    })
}
