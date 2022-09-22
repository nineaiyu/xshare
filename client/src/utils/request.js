import axios from 'axios'
import {ElMessage, ElMessageBox} from 'element-plus'
import {getAccessToken, getRefreshToken, removeToken, setToken} from '@/utils/auth'
import {refreshToken} from "@/api/user";
import {tokenStore} from "@/store";

// create an axios instance
const service = axios.create({
    // baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
    baseURL: 'http://127.0.0.1:8000/api/v1', // url = base url + request url
    // withCredentials: true, // send cookies when cross-domain requests
    timeout: 60000 // request timeout
})

// request interceptor
service.interceptors.request.use(
    config => {
        // do something before request is sent
        config.headers['Authorization'] = 'Bearer ' + getAccessToken()
        return config
    },
    error => {
        // do something with request error
        console.log(error) // for debug
        return Promise.reject(error)
    }
)

// response interceptor
service.interceptors.response.use(
    /**
     * If you want to get http information such as headers or status
     * Please return  response => response
     */

    /**
     * Determine the request status by custom code
     * Here is just an example
     * You can also judge the status by HTTP Status Code
     */
    response => {
        const res = response.data

        // if the custom code is not 1000, it is judged as an error.
        if (res.code !== 1000) {


            if (res.code === 9999) {
                setTimeout(() => {
                    location.reload()
                }, 500)
            } else if (res.code === 5000) {
                ElMessage({
                    message: res.result || 'Error',
                    type: 'error',
                    duration: 5 * 1000
                })
            } else
                ElMessage({
                    message: res.msg || 'Error',
                    type: 'error',
                    duration: 5 * 1000
                })

            // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
            if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
                // to re-login
                ElMessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
                    confirmButtonText: 'Re-Login',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }).then(() => {
                    // store.dispatch('user/resetToken').then(() => {
                    //   location.reload()
                    // })
                })
            }
            return Promise.reject(res)
        } else {
            return res
        }
    },
    error => {
        const token = tokenStore()
        if (error.response.status === 401) {
            const RefreshToken = getRefreshToken()
            if (RefreshToken) {
                token.count += 1
                refreshToken({refresh: RefreshToken}).then(res => {
                    setToken(res.data)
                    if (token.count > 1) {
                        removeToken()
                        token.count = 0
                    } else {
                        location.reload()
                    }
                }).catch(() => {
                    removeToken()
                    token.count = 0
                    location.reload()
                })
            }
        }
        console.log('err' + error) // for debug
        ElMessage({
            message: error.message,
            type: 'error',
            duration: 5 * 1000
        })
        return Promise.reject(error)
    }
)

export default service
