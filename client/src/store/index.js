import {defineStore} from 'pinia'
import {getAccessToken, getRefreshToken, setToken} from '@/utils/auth'
import {getUserInfo, login} from '@/api/user'
import {multiUpload} from "@/utils/upload";

export const userinfoStore = defineStore('userinfo', {
    state: () => ({
        username: '',
        first_name: '',
        email: '',
        last_login: '',
        token: getAccessToken(),
        refreshToken: getRefreshToken()
    }),
    actions: {
        async login(userInfo, loginData) {
            const {username, password} = userInfo
            return new Promise((resolve, reject) => {
                login({
                    username: username.trim(), password: password.trim(), token: loginData.token,
                    client_id: loginData.client_id
                }).then(response => {
                    const {data} = response
                    setToken(data)
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        async getUserInfo() {
            return new Promise((resolve, reject) => {
                getUserInfo().then(response => {
                    const {data} = response
                    resolve(data)
                }).catch(error => {
                    reject(error)
                })
            })
        }
    },
})


export const menuStore = defineStore('menu', {
    state: () => ({
        activeIndex: '',
    }),
})
export const tokenStore = defineStore('token', {
    state: () => ({
        count: 0,
    }),
})

export const uploadProgressStore = defineStore('progress', {
    state: () => ({
        progress: '',
        speeds: '',
        percent: []
    }),
})


export const uploadStore = defineStore('upload', {
    state: () => ({
        multiFileList: [],
        maximum: 3,
        promise: []
    }),
    actions: {
        upload() {
            if (this.multiFileList.length > 0) {
                multiUpload()
            }
        }
    }
})
