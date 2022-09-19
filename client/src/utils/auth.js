import Cookies from 'js-cookie'

const TokenKey = 'xshare-Token'
const RefreshTokenKey = 'xshare-Refresh-Token'

export function getToken() {
    return Cookies.get(TokenKey)
}

export function getRefreshToken() {
    return Cookies.get(RefreshTokenKey)
}

export function setToken(token, refreshToken) {
    Cookies.set(TokenKey, token)
    return Cookies.set(RefreshTokenKey, refreshToken)
}


export function removeToken() {
    Cookies.remove(TokenKey)
    return Cookies.remove(RefreshTokenKey)
}
