import {createRouter, createWebHashHistory} from 'vue-router'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
// import { ElMessage } from 'element-plus'
import {getToken} from '@/utils/auth'

import {menuStore, userinfoStore} from "@/store";


NProgress.configure({showSpinner: false})

const whiteList = ['/login', '/auth-redirect'] // no redirect whitelist

const routes = [
    {
        path: '/',
        name: 'index',
        redirect: {name: 'hello'}
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
    }

]

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes
});

router.beforeEach(async (to, from, next) => {
    // start progress bar
    NProgress.start()
    const menuList = ['lobby', 'upload', 'files', 'drive']
    const menu = menuStore()
    if (menuList.indexOf(to.name) !== -1) {
        menu.activeIndex = to.name
    }

    const hasToken = getToken()
    if (hasToken) {
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
