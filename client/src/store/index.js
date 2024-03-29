import {defineStore} from 'pinia'
import {setToken} from '@/utils/auth'
import {getUserInfo, login, register} from '@/api/user'

export const userinfoStore = defineStore('userinfo', {
    state: () => ({
        username: '',
        first_name: '',
        email: '',
        last_login: '',
        expired_time: '',
    }),
    actions: {
        async login(userInfo, loginData) {
            const {username, password} = userInfo
            return new Promise((resolve, reject) => {
                login({
                    username: username.trim(), password: password.trim(), token: loginData.token,
                    client_id: loginData.client_id
                }).then(async response => {
                    const {data} = response
                    setToken(data)
                    const userinfo = await this.getUserInfo()
                    this.$patch(userinfo)
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        async register(userInfo, loginData) {
            const {username, password} = userInfo
            return new Promise((resolve, reject) => {
                register({
                    username: username.trim(), password: password.trim(), token: loginData.token,
                    client_id: loginData.client_id
                }).then(async response => {
                    const {data} = response
                    setToken(data)
                    const userinfo = await this.getUserInfo()
                    this.$patch(userinfo)
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


export const uploadStore = defineStore('upload', {
    state: () => ({
        multiFileList: [],
        processNumber: 3,
        promise: []
    }),
    actions: {
        init() {
            this.promise = []
            this.multiFileList = []
        }
    }
})
