<template>
  <div class="header">
    <el-menu
        :default-active="store.activeIndex"
        :ellipsis="false"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
    >
      <div class="flex-grow"/>
      <el-menu-item index="index">Xshare</el-menu-item>
      <div class="flex-grow"/>

      <el-menu-item index="lobby">文件大厅</el-menu-item>
      <el-menu-item index="upload">发送文件</el-menu-item>
      <el-menu-item index="share">分享记录</el-menu-item>
      <el-menu-item index="files">文件管理</el-menu-item>
      <el-menu-item index="drive">云盘管理</el-menu-item>
      <div class="flex-grow"/>

      <el-sub-menu index="6">
        <template #title>您好，谁许时光</template>
        <el-menu-item index="userinfo">个人中心</el-menu-item>
        <!--        <el-menu-item index="drive">空间管理</el-menu-item>-->
        <el-menu-item index="logout">注销登录</el-menu-item>
      </el-sub-menu>
      <div class="flex-grow"/>


    </el-menu>
  </div>
</template>

<script>
import {menuStore} from "@/store";

export default {
  name: "ShareHeader",
  data() {
    const store = menuStore()
    return {
      store
    }
  }, methods: {
    handleSelect(key) {
      this.$router.push({name: key})
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

</style>
