<template>
  <preview-video v-model:video-visible="videoVisible" :video-src="videoSrc" :video-title="videoTitle"></preview-video>
  <el-row style="text-align: center;">
    <el-col :span="11">
      <el-card shadow="hover">
        <template #header>
          最新文件分享
        </template>
        <el-scrollbar v-loading="loading" style="height: calc(100vh - 300px);">
          <div v-for="share in share_data" :key="share.short" class="scrollbar-item">
            <el-popover
                :width="200"
                title="分享信息"
                trigger="hover"
            >
              <el-form class="shareinfo">
                <el-form-item label="分享连接：">
                  <el-tooltip content="点击访问分享下载页">
                    <el-link :underline="false" @click="$router.push({name:'short',params :{short:share.short}})">
                      {{ share.short }}
                    </el-link>
                  </el-tooltip>
                </el-form-item>
                <el-form-item label="文件数量：">
                  <el-tag type="success">{{ share.count }}</el-tag>
                </el-form-item>
                <el-form-item label="文件大小：">
                  <el-tag>{{ diskSize(share.size) }}</el-tag>
                </el-form-item>
                <el-form-item label="分享时间：">
                  <el-tag type="warning">{{ share.created_time.split('T')[0] }}</el-tag>
                </el-form-item>
                <el-form-item label="描述信息："></el-form-item>
                <p class="share-desc">{{ share.description }}</p>

              </el-form>
              <template #reference>
                <div class="share-content" style="vertical-align:middle;">
                  <el-link :underline="false" class="short"
                           @click="$router.push({name:'short',params :{short:share.short}})">{{ share.short }}
                  </el-link>
                  <span class="point">♥</span>
                  <span class="desc"> {{ getDesc(share) }}</span>
                </div>
              </template>
            </el-popover>
            <span class="time">{{ share.created_time.split('T')[0] }}</span>
          </div>
        </el-scrollbar>
      </el-card>
    </el-col>
    <el-col :push="2" :span="11">
      <el-card shadow="hover">
        <template #header>
          文件下载榜单
        </template>
        <el-scrollbar v-loading="loading" style="height: calc(100vh - 300px);">
          <div v-for="file in file_data" :key="file.file_id" class="scrollbar-item">
            <el-popover
                :width="200"
                title="文件信息"
                trigger="hover"
            >
              <el-form class="shareinfo">
                <el-form-item label="下载连接：">
                  <el-link :underline="false" @click="downloadFile(file)">点击下载</el-link>
                </el-form-item>
                <el-form-item v-if="file.category==='video'" label="播放视频：">
                  <el-link :underline="false" @click="preview(file)">点击播放</el-link>
                </el-form-item>
                <el-form-item label="下载次数：">
                  <el-tag type="success">{{ file.downloads }}</el-tag>
                </el-form-item>
                <el-form-item label="文件大小：">
                  <el-tag>{{ diskSize(file.size) }}</el-tag>
                </el-form-item>
                <el-form-item label="分享时间：">
                  <el-tag type="warning">{{ file.created_at.split('T')[0] }}</el-tag>
                </el-form-item>
                <el-form-item label="描述信息："></el-form-item>
                <p class="share-desc">{{ file.description }}</p>

              </el-form>
              <template #reference>
                <div class="share-content" style="vertical-align:middle;">
                  <el-link :underline="false" class="file-desc desc"> {{ file.name }}</el-link>
                </div>
              </template>
            </el-popover>
            <span class="time">{{ file.created_at.split('T')[0] }}</span>
          </div>
        </el-scrollbar>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>

import {getLobby} from "@/api/lobby";
import {diskSize, downloadFile} from "@/utils";
import {getFileUrl} from "@/api/short";
import {ElMessage} from "element-plus";

export default {
  name: "FileLobby",
  components: {},
  data() {
    return {
      share_data: [],
      file_data: [],
      show: true,
      loading: false,
      videoSrc: '',
      videoTitle: '',
      videoVisible: false
    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    diskSize,
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
    initData() {
      this.loading = true
      getLobby().then(res => {
        this.file_data = res.data.file_data
        this.share_data = res.data.share_data
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    getDesc(share) {
      let desc = share.description
      if (desc && desc.length > 0) {
        return `描述信息：${desc}`
      } else {
        return `文件数量：${share.count} 文件大小：${this.diskSize(share.size)}`
      }
    },
    downloadFile(file) {
      getFileUrl({auth_infos: [{file_id: file.file_id, token: file.token}]}).then(res => {
        res.data.forEach(url => {
          downloadFile(url.download_url)
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.scrollbar-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 40px;
  margin: 5px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  /*color: var(--el-color-primary);*/
}

.shareinfo {
  .el-form-item {
    margin-bottom: 0;
  }
}

.share-content {
  font-size: 15px;

  .short {
    width: 80px;
    display: inline-block;
    margin-top: -10px;
  }

  .point {
    display: inline-block;
    align-items: center;
    padding: 0 5px;
    color: red;
    font-size: 25px;
  }

  .desc {
    font-size: 14px;
    text-align: left;
    width: 300px;
    display: inline-block;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: #0873c7;
  }
}

.time {
  margin-right: 10px;
  font-size: 13px;
}

.share-desc {
  font-size: 14px;
  text-indent: 80px;
  margin-top: -28px;
  line-height: 26px;
  color: #0873c7;
}

.file-desc {
  margin-left: 10px;
  width: 390px !important;
}
</style>
