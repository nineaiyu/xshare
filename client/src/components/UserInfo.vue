<template>
  <el-form :model="userinfo" label-position="left"
           label-width="80px"
           style="max-width: 45%;margin: 0 auto">
    <el-form-item label="用户名">
      <el-link :underline="false">{{ userinfo.username }}</el-link>
    </el-form-item>
    <el-divider/>
    <!--    <el-form-item label="邮箱">-->
    <!--      <el-link :underline="false">{{ userinfo.email }}</el-link>-->
    <!--    </el-form-item>-->
    <!--    <el-divider/>-->

    <el-form-item label="最近登录">
      <el-link :underline="false">{{ formatTime(userinfo.last_login) }}</el-link>
    </el-form-item>

    <el-form-item v-if="userinfo.expired_time!=='1'" label="失效时间">
      <el-link :underline="false">
        <el-tooltip content="游客用户，失效时间内未登录，系统将自动清理该用户所有数据">
          {{ formatTime(userinfo.expired_time) }}
        </el-tooltip>
      </el-link>
    </el-form-item>
  </el-form>
</template>

<script>
import {userinfoStore} from "@/store";
import {formatTime} from "@/utils";

export default {
  name: "UserInfo",
  data() {
    const userinfo = userinfoStore()
    return {
      userinfo
    }
  }, methods: {
    formatTime,
  }
}
</script>

<style lang="scss" scoped>

</style>
