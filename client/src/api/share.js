import request from '@/utils/request'


export function getShare(params) {
    return request({
        url: '/share',
        method: 'get',
        params: params
    })
}

export function addShare(data) {
    return request({
        url: '/share',
        method: 'post',
        data: data
    })
}


export function delShare(id) {
    return request({
        url: '/share/' + id,
        method: 'delete',
    })
}

export function updateShare(params) {
    return request({
        url: '/share/' + params.id,
        method: 'put',
        data: params
    })
}

export function delManyShare(share_id_list) {
    return request({
        url: '/many/share',
        method: 'post',
        data: {action: 'delete', share_id_list}
    })
}


