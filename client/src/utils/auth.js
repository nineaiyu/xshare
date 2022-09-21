import Cookies from 'js-cookie'

const TokenKey = 'xshare-Token'
const RefreshTokenKey = 'xshare-Refresh-Token'

export function getAccessToken() {
    return Cookies.get(TokenKey)
}

export function getRefreshToken() {
    return Cookies.get(RefreshTokenKey)
}

export function setAccessToken(token, expires = 864e3) {
    Cookies.remove(TokenKey)
    return Cookies.set(TokenKey, token, {expires: new Date(Date.now() + 1000 * expires)})
}

export function setRefreshToken(token, expires = 864e3) {
    return Cookies.set(RefreshTokenKey, token, {expires: new Date(Date.now() + 1000 * expires)})
}


export function removeToken() {
    Cookies.remove(TokenKey)
    return Cookies.remove(RefreshTokenKey)
}

export function setToken(data) {
    if (data.access && data.access_token_lifetime) {
        setAccessToken(data.access, data.access_token_lifetime)
    }
    if (data.refresh && data.refresh_token_lifetime) {
        setRefreshToken(data.refresh, data.refresh_token_lifetime)
    }
}
