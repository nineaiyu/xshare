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
      <el-menu-item index="uploads">发送文件</el-menu-item>
      <el-menu-item index="files">文件管理</el-menu-item>
      <el-menu-item index="drive">云盘管理</el-menu-item>
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
      this.$router.push({name: key})
    },
    logout() {
      logout({refresh: getRefreshToken()}).then(() => {
        removeToken()
        ElMessage.success('账户注销成功')
        this.$router.push({name: 'login'})
      })
    }
  }, mounted() {
  }
}
</script>

<style scoped>
.header {
  background-color: #fdfdfe;
  height: 60px;
  margin: -8px -8px 8px -8px;
  /*box-shadow: 0 1px 5px 0 rgb(0 0 0 / 15%);*/
  line-height: 60px;
}

.flex-grow {
  flex-grow: 1;
}

.ly-header{
  background-image: linear-gradient(to right, #92fe9d 0%, #00c9ff 100%);
}





</style>
