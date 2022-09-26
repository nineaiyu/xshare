<template>
  <el-row style="text-align: center;">
    <el-col :span="11">
      <el-card shadow="hover">
        <template #header>
          最新文件分享
        </template>
        <el-scrollbar style="height: calc(100vh - 300px);">
         <span v-for="share in share_data" :key="share.short" class="scrollbar-demo-item">
           {{ share.short }} {{ share.count }} {{ share.size }} {{ share.created_time }} {{ share.description }}
         </span>
        </el-scrollbar>
      </el-card>
    </el-col>
    <el-col :push="2" :span="11">
      <el-card shadow="hover">
        <template #header>
          文件下载榜单
        </template>
        <el-scrollbar style="height: calc(100vh - 300px);">
         <span v-for="file in file_data" :key="file.file_id" class="scrollbar-demo-item">
           {{ file.name }} {{ file.downloads }} {{ file.size }} {{ file.created_at }} {{ file.description }}
         </span>
        </el-scrollbar>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>

import {getLobby} from "@/api/lobby";

export default {
  name: "FileLobby",
  components: {},
  data() {

    return {
      share_data: [],
      file_data: []
    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    initData() {
      getLobby().then(res => {
        this.file_data = res.data.file_data
        this.share_data = res.data.share_data
      })
    }
  }
}
</script>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  /*justify-content: center;*/
  height: 40px;
  margin: 5px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  /*color: var(--el-color-primary);*/
}
</style>
