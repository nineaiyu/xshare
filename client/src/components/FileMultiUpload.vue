<template>
  <el-container>
    <el-main style="text-align: center;">
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
      <el-table :data="upload.multiFileList" border stripe style="width: 100%">
        <el-table-column align="center" label="文件名" prop="progress.file_name" width="500"/>
        <el-table-column :formatter="fileSize" align="center" label="文件大小" prop="progress.file_size"/>
        <el-table-column :formatter="fileProgress" align="center" label="上传进度" prop="progress.progress"/>
        <el-table-column align="center" label="上传速度" prop="progress.speed"/>
      </el-table>
    </el-main>
  </el-container>
</template>

<script>
import {uploadProgressStore, uploadStore} from "@/store";
import {diskSize} from "@/utils";
import {addUploadFile} from "@/utils/upload";

export default {
  name: "FileMultiUpload",
  data() {
    const colors = [
      {color: '#f56c6c', percentage: 20},
      {color: '#e6a23c', percentage: 40},
      {color: '#5cb87a', percentage: 60},
      {color: '#1989fa', percentage: 80},
      {color: '#6f7ad3', percentage: 100},
    ]
    const progress = uploadProgressStore()
    const upload = uploadStore()
    return {
      progress,
      colors,
      rawFile: {name: '', size: 0},
      upload,
    }
  }, methods: {
    async beforeUpload(raw) {
      addUploadFile(raw)
      return false
    },
    fileSize(row) {
      return diskSize(row.progress.file_size)
    },
    fileProgress(row) {
      return row.progress.progress + '%'
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
