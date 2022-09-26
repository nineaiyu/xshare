import request from '@/utils/request'


export function getLobby(params) {
    return request({
        url: '/lobby',
        method: 'get',
        params: params
    })
}
