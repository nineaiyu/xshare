<template>
  <div style="text-align: center;">
    <el-card shadow="hover" style="max-width: 50%;margin: 0 auto">
      <el-avatar :size="80" :src="createBase64(userinfo.first_name)"/>
      <el-card style="max-width: 50%;margin: 10px auto">
        {{ userinfo.first_name }}
      </el-card>
    </el-card>
  </div>
</template>

<script>
import {userinfoStore} from "@/store";
import {createBase64} from "@/utils";

export default {
  name: "UserInfo",
  data() {
    const userinfo = userinfoStore()

    return {
      userinfo
    }
  }, methods: {
    createBase64
  }
}
</script>

<style scoped>

</style>
