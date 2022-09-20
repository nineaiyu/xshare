import request from '@/utils/request'


export function getFileShare(short) {
    return request({
        url: '/short',
        method: 'get',
        params: {short: short}
    })
}
