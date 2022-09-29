<template>
  <div style="text-align: center;">
    <el-card shadow="hover" style="max-width: 70%;margin: 0 auto">
      <div class="username">
        <div style="margin-top: 20px">
          <el-avatar :size="80" :src="createBase64(userinfo.first_name)"/>
        </div>
        <input v-model="userinfo.first_name" maxlength="100" @focusout="update"/>
      </div>
      <el-divider/>
      <router-view/>
    </el-card>
  </div>
</template>

<script>
import {userinfoStore} from "@/store";
import {createBase64} from "@/utils";
import {updateUserInfo} from "@/api/user";
import {ElMessage} from "element-plus";

export default {
  name: "UserBase",
  data() {
    const userinfo = userinfoStore()

    return {
      userinfo
    }
  }, methods: {
    createBase64,
    update() {
      updateUserInfo({first_name: this.userinfo.first_name}).then(() => {
        ElMessage.success("昵称更新成功")
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.username {
  max-width: 60%;
  margin: 10px auto;

  input {
    text-align: center;
    color: #6983fc;
    margin: 20px;
    border: none;
    line-height: 50px;
    background-color: transparent;
    font-size: 20px;
    outline-color: rgba(88, 88, 152, 0.56);
  }

}
</style>
