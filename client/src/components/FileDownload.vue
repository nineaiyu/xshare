<template>
  <el-container style="max-width: 880px;text-align: center;margin: 0 auto">
    <el-main>
      <el-row style="height: 200px;margin-bottom: 20px">
        <el-col :span="8">

          <el-card shadow="hover" style="text-align: left;height:100%">
            <template #header>
              <div class="card-header">
                <span>分享信息</span>
              </div>
            </template>
            <el-form :model="shareInfo" label-position="left" label-width="80px">
              <el-form-item label="文件数量">
                {{ shareInfo.file_info_list.length }}
              </el-form-item>
              <el-form-item label="文件大小">
                {{ diskSize(shareInfo.size) }}
              </el-form-item>
              <el-form-item label="到期时间">
                {{ formatTime(shareInfo.expired_time) }}
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
        <el-col :span="8" style="display: flex;flex-direction: column;justify-content: space-around">
          <div>
            <el-avatar :size="80" :src="userInfo.head_img"/>
          </div>
          <div><i style="color: teal">{{ userInfo.first_name }}</i></div>
          <div style="margin: 0 10px">
            <div v-if="shareInfo.need_password">
              <el-row>
                <el-col :span="14">
                  <el-input
                      v-model="password"
                      clearable
                      placeholder="请输入密码"
                      prefix-icon="Lock"/>
                </el-col>
                <el-col :span="1"></el-col>
                <el-col :span="6">
                  <el-button @click="getShareInfo">提取文件</el-button>
                </el-col>
              </el-row>
            </div>
            <el-button v-else color="#626aef" icon="Download" plain @click="downloadShare">全部下载</el-button>
          </div>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" style="text-align: left;height:100%">
            <template #header>
              <div class="card-header">
                <span>描述信息</span>
              </div>
            </template>
            <el-form :model="shareInfo" label-position="left" label-width="80px">
              {{ shareInfo.description }}
            </el-form>
          </el-card>
        </el-col>
      </el-row>
      <el-card shadow="hover">
        <el-table :data="shareInfo.file_info_list" border stripe>
          <el-table-column type="index"/>
          <el-table-column align="center" label="文件名" prop="name">
            <template #default="scope">
              <el-link :underline="false">{{ scope.row.name }}</el-link>
            </template>
          </el-table-column>
          <el-table-column :formatter="sizeFormatter" align="center" label="文件大小" prop="size" width="90"/>

          <el-table-column :formatter="uptimeFormatter" align="center" label="上传时间" prop="created_at"/>
          <el-table-column align="center" label="下载次数" prop="downloads" width="90"/>
          <el-table-column align="center" label="备注" prop="description"/>
          <el-table-column align="center" label="操作" width="110">
            <template #default="scope">
              <el-button size="small" @click="downloadFile(scope.row.id)">下载文件</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
import {getFileShare} from "@/api/download";
import {diskSize, downloadFile, formatTime} from "@/utils";
import {downloadManyFile, getDownloadUrl} from "@/api/file";

export default {
  name: "FileDownload",
  data() {
    return {
      short: '',
      password: '',
      shareInfo: {
        file_info_list: []
      },
      userInfo: {
        head_img: '',
        first_name: ''
      }
    }
  },
  methods: {
    getFileIdList() {
      let file_id_list = []
      this.shareInfo.file_info_list.forEach(res => {
        file_id_list.push(res.file_id)
      })
      return file_id_list
    },
    downloadShare() {
      downloadManyFile(this.getFileIdList()).then(res => {
        res.data.forEach(url => {
          downloadFile(url.download_url)
        })
      })
    },
    downloadFile(id) {
      getDownloadUrl(id).then(res => {
        downloadFile(res.data.download_url)
      })
    },
    diskSize,
    formatTime,
    getShareInfo() {
      getFileShare({short: this.short, password: this.password}).then(res => {
        this.userInfo = res.data.user_info
        this.shareInfo = res.data.share_info
        if (this.shareInfo.file_info_list.length > 0) {
          this.shareInfo.need_password = false
        }
      })
    }, uptimeFormatter(row) {
      return formatTime(row.created_at)
    }, sizeFormatter(row) {
      return diskSize(row.size)
    }
  },
  mounted() {
    this.short = this.$route.params.short
    this.password = this.$route.query.password
    this.getShareInfo()
  }
}
</script>

<style scoped>
* {
  font-size: 14px;
}

.el-form-item {
  margin-bottom: 2px;
}
</style>
