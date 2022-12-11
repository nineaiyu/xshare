<template>
  <el-container style="max-width: 880px;text-align: center;margin: 0 auto">
    <preview-video v-model:video-visible="videoVisible" :video-src="videoSrc" :video-title="videoTitle"></preview-video>
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
            <el-avatar :size="80" :src="createBase64(first_name)"/>
          </div>
          <div><i style="color: teal">{{ first_name }}</i></div>
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
            <el-button v-else color="#626aef" icon="Download" plain @click="downloadFile(shareInfo.file_info_list)">
              全部下载
            </el-button>
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
              <el-tooltip
                  v-if="scope.row.category==='video'"
                  content="点击播放视频"
                  placement="top-start"
              >
                <el-link :underline="false" @click="preview(scope.row)">{{ scope.row.name }}</el-link>
              </el-tooltip>
              <span v-else>
          {{ scope.row.name }}
        </span>
            </template>
          </el-table-column>
          <el-table-column :formatter="sizeFormatter" align="center" label="文件大小" prop="size" width="90"/>

          <el-table-column :formatter="uptimeFormatter" align="center" label="上传时间" prop="created_at"/>
          <el-table-column align="center" label="下载次数" prop="downloads" width="90"/>
          <el-table-column align="center" label="备注" prop="description"/>
          <el-table-column align="center" label="操作" width="110">
            <template #default="scope">
              <el-button size="small" @click="downloadFile([scope.row])">下载文件</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
import {getFileShare, getFileUrl} from "@/api/short";
import {createBase64, diskSize, downloadFile, formatTime} from "@/utils";
import PreviewVideo from "@/components/base/PreviewVideo";
import {ElMessage} from "element-plus";

export default {
  name: "FileDownload",
  data() {
    return {
      short: '',
      password: '',
      shareInfo: {
        file_info_list: []
      },
      first_name: '',
      videoSrc: '',
      videoTitle: '',
      videoVisible: false
    }
  },
  components: {
    PreviewVideo
  },
  methods: {
    createBase64,
    preview(row) {
      getFileUrl({auth_infos: [{file_id: row.file_id, token: row.token, act: 'preview'}]}).then(res => {
        if (res.code === 1000) {
          if (res.data.preview_url === "") {
            ElMessage.error("文件违规")
            return
          }
          this.videoSrc = res.data.preview_url
          this.videoTitle = row.name
          this.videoVisible = true
        }
      })
    },
    makeDownloadAuth(rows) {
      let auth = []
      rows.forEach(res => {
        auth.push({file_id: res.file_id, token: res.token})
      })
      return auth
    },
    getFileIdList() {
      let file_id_list = []
      this.shareInfo.file_info_list.forEach(res => {
        file_id_list.push(res.file_id)
      })
      return file_id_list
    },
    downloadFile(rows) {
      getFileUrl({auth_infos: this.makeDownloadAuth(rows)}).then(res => {
        res.data.forEach(url => {
          downloadFile(url.download_url)
        })
      })
    },
    diskSize,
    formatTime,
    getShareInfo() {
      getFileShare({short: this.short, password: this.password}).then(res => {
        this.first_name = res.data.first_name
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
