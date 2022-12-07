<template>
  <div class="header">
    <el-menu
        :default-active="store.activeIndex"
        :ellipsis="false"
        class="el-menu-demo ly-header"
        mode="horizontal"
        @select="handleSelect"
    >
      <div class="flex-grow"/>
      <el-menu-item index="index">Xshare</el-menu-item>
      <div class="flex-grow"/>

      <el-menu-item index="lobby">文件大厅</el-menu-item>
      <el-menu-item index="share">分享记录</el-menu-item>
      <el-menu-item index="uploads">上传文件</el-menu-item>
      <el-menu-item index="files">文件管理</el-menu-item>
      <el-menu-item index="drive">云盘管理</el-menu-item>
      <el-menu-item index="github">Github</el-menu-item>
      <div class="flex-grow"/>

      <el-sub-menu index="6">
        <template #title>{{ getTitleName() }}</template>
        <el-menu-item index="userinfo">
          <el-icon>
            <UserFilled/>
          </el-icon>
          个人中心
        </el-menu-item>
        <el-menu-item index="password">
          <el-icon>
            <Unlock/>
          </el-icon>
          修改密码
        </el-menu-item>
        <el-menu-item @click="logout">
          <el-icon>
            <SwitchFilled/>
          </el-icon>
          注销登录
        </el-menu-item>
      </el-sub-menu>
      <div class="flex-grow"/>


    </el-menu>
  </div>
</template>

<script>
import {menuStore, userinfoStore} from "@/store";
import {logout} from "@/api/user";
import {getRefreshToken, removeToken} from "@/utils/auth";
import {ElMessage} from "element-plus";

export default {
  name: "ShareHeader",
  data() {
    const store = menuStore()
    const userinfo = userinfoStore()
    return {
      store,
      userinfo
    }
  }, methods: {
    getTitleName() {
      if (this.userinfo.first_name) {
        return this.userinfo.first_name
      }
      return this.userinfo.username
    },
    handleSelect(key) {
      if (key === 'github') {
        window.open('https://github.com/nineaiyu/xshare', '_blank', '');
      } else {
        this.$router.push({name: key})
      }
    },
    logout() {
      const refresh = getRefreshToken()
      if (refresh) {
        logout({refresh}).then(() => {
          removeToken()
          ElMessage.success('账户注销成功')
          this.$router.push({name: 'login'})
        }).catch(() => {
          removeToken()
        })
      }
    }
  }, mounted() {
  }
}
</script>

<style scoped>
.header {
  height: 60px;
  line-height: 60px;
}

.flex-grow {
  flex-grow: 1;
}

.ly-header {
  background-image: linear-gradient(to right, #eaebee 0%, #ace0f9 100%);
}


</style>
