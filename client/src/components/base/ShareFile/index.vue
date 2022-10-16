<template>
  <el-dialog v-model="showVisible" :close-on-click-modal="false" center
             draggable
             title="创建分享连接"
             width="600px">
    <el-form
        :model="formShare"
        label-position="right"
        label-width="100px"
        style="max-width: 480px"
    >
      <el-form-item label="文件数量">
        <el-tag>{{ fileIdList.length }}</el-tag>
      </el-form-item>
      <el-form-item label="下载密码">
        <div style="margin-right: 20px">
          <el-input v-model="formShare.password"
                    clearable
                    maxlength="16"
                    placeholder="默认无密码"
                    show-word-limit
          />
        </div>
        <el-button @click="makeRandomPwd">生成</el-button>
      </el-form-item>
      <el-form-item label="过期时间">
        <el-date-picker
            v-model="formShare.expired_time"
            :shortcuts="shortcuts"
            placeholder="请选择过期时间"
            type="datetime"
            value-format="x"
        />
      </el-form-item>
      <el-form-item label="备注信息">
        <el-input v-model="formShare.description"
                  :autosize="{ minRows: 3}"
                  clearable
                  maxlength="220"
                  placeholder="请添加备注信息"
                  show-word-limit
                  type="textarea"/>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="showVisible = false">取消</el-button>
        <el-button type="primary" @click="shareManyFileFun">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import {addShare} from "@/api/share"
import {ElMessage, ElNotification} from "element-plus"
import {getLocationOrigin, getRandomStr} from "@/utils";

export default {
  name: "ShareFile",
  data(){
    return {
      formShare: {
        expired_time: (new Date()).getTime() + 3600 * 1000 * 24 * 7,
        password: '',
        description: '',
      },
    }
  },
  computed: {
    showVisible:{
      get() {
        return this.shareVisible
      },
      set(value){
        this.$emit('update:shareVisible', value)
      }
    }
  },
  props:{
    shareVisible:{},
    fileIdList:{
      type:Array,
      required:true
    },
    shortcuts:{
      type:Array,
      default() {
        return [
          {
            text: '今天',
            value: new Date(),
          },
          {
            text: '三天',
            value: () => {
              const date = new Date()
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 3)
              return date
            },
          },
          {
            text: '一星期',
            value: () => {
              const date = new Date()
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 7)
              return date
            },
          }, {
            text: '一年',
            value: () => {
              const date = new Date()
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 365)
              return date
            },
          },
        ];
      }
    }
  }, methods:{
    makeShortUrl(short) {
      return getLocationOrigin() + short
    },
    shareManyFileFun() {
      addShare({file_id_list: this.fileIdList, share_info: this.formShare}).then((res) => {
        ElMessage.success("分享成功")
        ElNotification({
          title: '分享成功',
          type:'success',
          dangerouslyUseHTMLString: true,
          message: `分享链接地址： <strong><a href="${this.makeShortUrl(res.data.short)}?password=${res.data.password}">${this.makeShortUrl(res.data.short)}?password=${res.data.password}</a></strong>`,
          duration:8000
        })
        this.showVisible = false
      }).catch(() => {
        this.showVisible = false
      })
    },
    makeRandomPwd(){
      this.formShare.password = getRandomStr(8)
    }
  },watch:{
    'shareVisible':function () {
      this.formShare.description=''
      this.formShare.password=''
    }
  }
}
</script>

<style scoped>

</style>