<template>
  <el-container>
    <el-main style="text-align: center;">

      <el-row>
        <el-col :span="12">
          <el-upload
              :before-upload="beforeUpload"
              action="#"
              class="upload"
              drag
              multiple
          >
            <el-icon class="el-icon--upload">
              <upload-filled/>
            </el-icon>
            <div class="el-upload__text">
              拖拽或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                请上传文件，仅支持上传文件，不支持文件夹
              </div>
            </template>
          </el-upload>

        </el-col>

        <el-col :span="12" style="height: calc(100vh - 180px);">
          <el-card shadow="hover">
            <template #header>
              <el-row>
                <el-col :span="18">
                  <div v-if="upload.multiFileList.length===0" style="text-align: left">
                    文件上传列表
                  </div>
                  <div v-else style="text-align: left">
                    <div v-if="getUploadingFile(upload.multiFileList).length > 0">文件上传中，还剩
                      {{ getUnUploadNumber(upload.multiFileList) }} 项，共 {{ upload.multiFileList.length }} 项
                    </div>
                    <span v-else>上传完成，共 {{ upload.multiFileList.length }} 项</span>
                  </div>
                </el-col>
                <el-col :span="5">
                  <el-tooltip content="同时上传任务数">
                    <el-input-number v-model="upload.processNumber" :max="10" :min="1" @change="handleChange"/>
                  </el-tooltip>
                </el-col>
              </el-row>

            </template>
            <ul class="infinite-list scroll">
              <li v-for="info in getUploadFile(upload.multiFileList)" :key="info.uid" class="infinite-list-item">
                <el-progress
                    :color="colors"
                    :percentage="info.progress.progress"
                    :stroke-width="50"
                    :text-inside="true">
                  <div style="width: 400px;">
                    <el-row>
                      <el-col :span="17">
                        <p style="overflow: hidden;text-overflow: ellipsis">{{ info.progress.file_name }}</p>
                        <p>{{ formatUpload(info.progress) }} - {{ info.progress.progress }}</p>
                      </el-col>

                      <el-col :span="7">
                        <el-row>
                          <el-col :span="20"><span style="line-height: 50px">{{ info.progress.speed }}</span></el-col>
                          <el-col :span="4">
                            <div v-if="info.progress.progress===100" style="line-height: 70px">
                              <el-icon :size="30">
                                <CircleCheck/>
                              </el-icon>
                            </div>
                            <div v-else style="line-height: 70px">
                              <el-tooltip v-if="[0,1].indexOf(info.status)!==-1" content="取消上传">
                                <el-icon :size="30" @click="cancelUpload(info)">
                                  <CircleClose/>
                                </el-icon>
                              </el-tooltip>
                              <el-tooltip v-else-if="info.status === 3 " content="重新上传">
                                <el-icon :size="30" @click="cancelUpload(info)">
                                  <Position/>
                                </el-icon>
                              </el-tooltip>
                            </div>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                  </div>
                </el-progress>
              </li>
            </ul>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import {uploadStore} from "@/store";
import {diskSize} from "@/utils";
import {addUploadFile, multiUpload} from "@/utils/upload";
import {ElMessage} from "element-plus";

export default {
  name: "FileMultiUpload",
  data() {
    const colors = [
      {color: '#a2c236', percentage: 20},
      {color: '#c2bf40', percentage: 40},
      {color: '#47c43e', percentage: 60},
      {color: '#24a016', percentage: 80},
      {color: '#23a871', percentage: 100},
    ]
    const upload = uploadStore()
    return {
      colors,
      rawFile: {name: '', size: 0},
      upload,
    }
  }, methods: {
    handleChange(num) {
      this.upload.processNumber = num
      multiUpload()
    },
    cancelUpload(info) {
      if (info.status === 3) {
        info.status = 0
        info.failTryCount = 3
        multiUpload()
      } else {
        info.status = 3
        info.progress.speed = '已手动取消'
        ElMessage.warning(`已手动取消上传 ${info.progress.file_name}`)
      }
    },
    beforeUpload(raw) {
      addUploadFile(raw)
      return false
    },
    formatUpload(info) {
      return `${diskSize(info.upload_size)}/${diskSize(info.file_size)}`
    },
    sortFileStatus(fileList) {
      return fileList.sort((a, b) => {
        return b.progress.upload_time - a.progress.upload_time
      })
    }, getUploadingFile(fileList) {
      return fileList.filter(res => {
        return res.status === 1
      })
    }, getUnUploadFile(fileList) {
      return fileList.filter(res => {
        return res.status !== 1
      })
    }, getUnUploadNumber(fileList) {
      return fileList.filter(res => {
        return res.status !== 2
      }).length
    }, getUploadFile(fileList) {
      let newFileList = []
      this.getUploadingFile(fileList).forEach(res => {
        newFileList.push(res)
      })
      this.getUnUploadFile(this.sortFileStatus(fileList)).forEach(res => {
        newFileList.push(res)
      })
      return newFileList
    }
  }, watch: {
    'uploa1d.multiFileList': {
      handler: function (upload) {
        upload.forEach(res => {
          if (res.status === 1) {
            console.log(res.progress.progress, res.progress.file_name, res.progress.speed)
          }
        })
      },
      deep: true
    }
  }
}
</script>

<style lang="scss" scoped>
.upload {
  width: 300px;
  margin: 200px auto;
}

:deep(.el-progress-bar__inner) {
  text-align: center;
  border-radius: 0;
}

:deep(.el-progress-bar__outer) {
  border-radius: 0;
}

.infinite-list {
  height: 60vh !important;
  overflow-y: scroll;
  padding: 0;
  margin: 0;
  list-style: none;
}

.infinite-list .infinite-list-item {
  align-items: center;
  justify-content: center;
  height: 50px;
  background: var(--el-color-primary-light-9);
  margin: 10px;
  color: var(--el-color-primary);
}

.infinite-list .infinite-list-item + .list-item {
  margin-top: 10px;
}

.scroll {
  height: 100%;
  /*这里需要首先固定高度*/
  overflow-y: scroll;
  /*我们一般习惯为纵向有滚动条，横向为固定*/
  overflow-x: hidden;
}

/* 修改滚动条样式 */
.scroll::-webkit-scrollbar {
  width: 3px;
  /*设置滚动条的宽度*/
}

/* 滚动区域的样式 */
.scroll::-webkit-scrollbar-thumb {
  border-radius: 10px;
  /*设置滚动条的圆角*/
  -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  /*设置内阴影*/
  background: rgb(81, 193, 238, 0.2);
  /*设置滚动条的颜色*/
}

/* 滚动条的背景样式 */
.scroll::-webkit-scrollbar-track {
  /* -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2); */
  border-radius: 0;
}

</style>
