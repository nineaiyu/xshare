<template>
  <el-container>
    <el-main style="text-align: center;">
      <el-upload
          :before-upload="beforeUpload"
          :disabled="progress.progress!==''&& progress.progress!==100"
          action="#"
          class="upload"
          drag
          multiple
      >
        <div v-if="!progress.progress">
          <el-icon class="el-icon--upload">
            <upload-filled/>
          </el-icon>
          <div class="el-upload__text">
            拖拽或 <em>点击上传</em>
          </div>
        </div>
        <div v-else>
          <el-progress :color="colors" :percentage="Number(progress.speed%100)" type="dashboard">
            <template #default>
              <span class="percentage-value">{{ diskSize(progress.speed) }}</span>
              <span class="percentage-label">上传中</span>
            </template>
          </el-progress>
          <!--          上传速度：{{progress.speed}}-->
        </div>
        <template #tip>
          <div class="el-upload__tip">
            请上传文件，仅支持上传文件，不支持文件夹
          </div>
          <div v-if="progress.progress" style="margin-top: 10px">
            <el-progress :indeterminate="true" :percentage="progress.progress"/>
            <div style="margin-top: 10px">
              {{ rawFile.name }}
            </div>
          </div>
        </template>
      </el-upload>

    </el-main>
  </el-container>
</template>

<script>
import {UploadFile} from "@/utils/upload";
import {uploadProgressStore} from "@/store";
import {diskSize} from "@/utils";

export default {
  name: "FileUpload",
  data() {
    const colors = [
      {color: '#f56c6c', percentage: 20},
      {color: '#e6a23c', percentage: 40},
      {color: '#5cb87a', percentage: 60},
      {color: '#1989fa', percentage: 80},
      {color: '#6f7ad3', percentage: 100},
    ]
    const progress = uploadProgressStore()
    return {
      progress,
      colors,
      rawFile: {name: '', size: 0}
    }
  }, methods: {
    diskSize,
    async beforeUpload(rawFile) {
      this.progress.progress = 0
      this.rawFile = rawFile
      await UploadFile(rawFile)
      return false
    }
  }
}
</script>

<style scoped>
.upload {
  width: 300px;
  margin: 100px auto
}

.percentage-value {
  display: block;
  margin-top: 10px;
  font-size: 28px;
}

.percentage-label {
  display: block;
  margin-top: 10px;
  font-size: 12px;
}

</style>
