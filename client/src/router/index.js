import {createRouter, createWebHashHistory} from 'vue-router'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import {getAccessToken, getRefreshToken, setToken} from '@/utils/auth'

import {menuStore, userinfoStore} from "@/store";
import {refreshToken} from "@/api/user";


NProgress.configure({showSpinner: false})

const whiteList = ['/login', '/auth-redirect'] // no redirect whitelist

const routes = [
    {
        path: '/',
        name: 'index',
        redirect: {name: 'lobby'}
    }, {
        path: '/HelloWorld',
        name: 'hello',
        component: () => import('@/components/HelloWorld')
    }, {
        path: '/login',
        name: 'login',
        component: () => import('@/components/UserLogin')
    }, {
        path: '/upload',
        name: 'upload',
        component: () => import('@/components/FileUpload')
    }, {
        path: '/lobby',
        name: 'lobby',
        component: () => import('@/components/FileLobby')
    }, {
        path: '/drive',
        name: 'drive',
        component: () => import('@/components/AliDrive')
    }, {
        path: '/share',
        name: 'share',
        component: () => import('@/components/FileShare')
    }, {
        path: '/files',
        name: 'files',
        component: () => import('@/components/FileManager')
    }, {
        path: '/user',
        name: 'user',
        component: () => import('@/components/UserBase'),
        children: [
            {
                path: 'info',
                name: 'userinfo',
                component: import('@/components/UserInfo'),
            }, {
                path: 'pwd',
                name: 'password',
                component: import('@/components/UserPwd'),
            },
        ]
    }, {
        path: '/:short',
        name: 'short',
        component: () => import('@/components/FileShort')
    }

]

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes
});

router.beforeEach(async (to, from, next) => {
    // start progress bar
    NProgress.start()

    if (to.name === 'short') {
        next()
        NProgress.done()
        return
    }

    const menuList = ['lobby', 'upload', 'files', 'drive', 'share', 'userinfo', 'password']
    const menu = menuStore()
    if (menuList.indexOf(to.name) !== -1) {
        menu.activeIndex = to.name
    }
    const accessToken = getAccessToken()
    if (accessToken) {
        if (to.path === '/login') {
            // if is logged in, redirect to the home page
            next({path: '/'})
            NProgress.done()
        } else {
            const store = userinfoStore()
            if (store.username) {
                next()
                NProgress.done()
            } else {
                const userinfo = await store.getUserInfo()
                store.$patch(userinfo)
                next()
                NProgress.done()
            }
        }
    } else {
        /* has no token*/
        const RefreshToken = getRefreshToken()
        if (RefreshToken) {
            const res = await refreshToken({refresh: RefreshToken})
            setToken(res.data)
            next()
            NProgress.done()
            return
        }

        if (whiteList.indexOf(to.path) !== -1) {
            // in the free login whitelist, go directly
            next()
            NProgress.done()
        } else {
            // other pages that do not have permission to access are redirected to the login page.
            next(`/login?redirect=${to.path}`)
            NProgress.done()
        }
    }
})

export default router;
