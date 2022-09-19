import {defineStore} from 'pinia'
// eslint-disable-next-line no-unused-vars
import {getRefreshToken, getToken, setToken} from '@/utils/auth'
// eslint-disable-next-line no-unused-vars
import {getUserInfo, login} from '@/api/user'

export const userinfoStore = defineStore('userinfo', {
    state: () => ({
        username: '',
        first_name: '',
        email: '',
        last_login: '',
        token: getToken(),
        refreshToken: getRefreshToken()
    }),
    getters: {
        // nickname: (state) => state.nickname,
        // avatar: (state) => state.avatar,
        // token: (state) => state.token,
    },
    actions: {
        async login(userInfo) {
            const {username, password} = userInfo
            return new Promise((resolve, reject) => {
                login({username: username.trim(), password: password.trim()}).then(response => {
                    const {data} = response
                    console.log(data)
                    this.token = data.access
                    this.refreshToken = data.refresh
                    setToken(data.access, data.refresh)
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

export const uploadProgressStore = defineStore('progress', {
    state: () => ({
        progress: '',
    }),
})
