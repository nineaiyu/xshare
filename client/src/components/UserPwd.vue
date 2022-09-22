<template>
  <el-form :model="userinfo" label-position="left"
           label-width="80px"
           style="max-width: 45%;margin: 0 auto">
    <el-form-item label="用户名">
      <el-link :underline="false">{{ userinfo.username }}</el-link>
    </el-form-item>
    <el-divider/>
    <el-form-item label="旧密码">
      <el-input v-model="password.old_password" clearable show-password></el-input>
    </el-form-item>
    <el-form-item label="新密码">
      <el-input v-model="password.new_password" clearable show-password></el-input>
    </el-form-item>
    <el-button @click="updatePwd">更新密码</el-button>
  </el-form>
</template>

<script>
import {userinfoStore} from "@/store";
import {updateUserInfo} from "@/api/user";
import {ElMessage} from "element-plus";

export default {
  name: "UserPwd",
  data() {
    const userinfo = userinfoStore()
    return {
      userinfo,
      password: {
        new_password: '',
        old_password: ''
      }
    }
  }, methods: {
    updatePwd() {
      if (this.password.new_password && this.password.old_password) {
        updateUserInfo(this.password).then(() => {
          ElMessage.success("密码修改成功")
        })
      } else {
        ElMessage.warning("请输入新密码")
      }

    }
  }
}
</script>

<style scoped>

</style>
