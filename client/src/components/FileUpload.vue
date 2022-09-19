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
          <div v-if="progress.progress" style="margin-top: 10px">
            <el-progress :percentage="progress.progress"/>
            <div style="margin-top: 10px">
              {{ rawfile.name }}
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

export default {
  name: "FileUpload",
  data() {
    const progress = uploadProgressStore()
    return {
      progress,
      rawfile: {name: '', size: 0}
    }
  }, methods: {
    async beforeUpload(rawFile) {
      this.progress.progress = 0
      this.rawfile = rawFile
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
</style>
