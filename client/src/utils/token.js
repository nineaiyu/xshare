import {getAccessToken, getRefreshToken, setToken} from "@/utils/auth";
import {refreshToken} from "@/api/user";

export async function getUsedAccessToken() {
    const accessToken = getAccessToken()
    if (accessToken) {
        return accessToken
    } else {
        const RefreshToken = getRefreshToken()
        if (RefreshToken) {
            const res = await refreshToken({refresh: RefreshToken})
            setToken(res.data)
            return getAccessToken()
        }
    }
}

