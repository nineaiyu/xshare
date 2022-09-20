<template>

  <el-dialog v-model="shareVisible" :close-on-click-modal="false" center
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
        <el-tag>{{ selectedData.length }}</el-tag>
      </el-form-item>
      <el-form-item label="下载连接">
        <el-input v-model="formShare.short"
                  clearable
                  maxlength="16"
                  minlength="6"
                  placeholder="空表示自动生成"
                  show-word-limit
        >
          <template #prepend>{{ prefixUrl }}</template>
        </el-input>
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
        <el-button @click="shareVisible = false">取消</el-button>
        <el-button type="primary" @click="shareManyFileFun">确定</el-button>
      </span>
    </template>
  </el-dialog>

  <div class="filter-container">
    <el-input v-model="listQuery.name" class="filter-item" clearable placeholder="文件名称" style="width: 140px;"
              @keyup.enter="handleFilter"/>
    <el-input v-model="listQuery.description" class="filter-item" clearable placeholder="备注" style="width: 140px;"
              @keyup.enter="handleFilter"/>
    <el-select v-model="listQuery.ordering" class="filter-item" style="width: 180px" @change="handleFilter">
      <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key"/>
    </el-select>
    <el-button class="filter-item" icon="Search" plain type="primary" @click="handleFilter">
      搜索&nbsp;&nbsp;&nbsp;
    </el-button>

    <div style="float: right">
      <el-button class="filter-item" icon="Delete" plain type="danger" @click="delManyFileFun">
        删除选中文件&nbsp;&nbsp;&nbsp;
      </el-button>
      <el-button class="filter-item" icon="Download" plain @click="downManyFileFun">
        下载选中文件&nbsp;&nbsp;&nbsp;
      </el-button>
      <el-button class="filter-item" icon="Share" plain @click="showShareDialog">
        分享选中文件&nbsp;&nbsp;&nbsp;
      </el-button>
    </div>
  </div>
  <el-table
      v-loading="isLoading"
      :data="tableData"
      border
      stripe
      style="width: 100%"
      @selection-change="handleSelectionChange"
  >
    <el-table-column align="center" type="selection" width="55"/>
    <el-table-column align="center" label="文件名" prop="name"/>
    <el-table-column :formatter="sizeFormatter" align="center" label="文件大小" prop="size" width="90"/>
    <el-table-column :formatter="timeFormatter" align="center" label="上传时间" prop="created_at"/>
    <el-table-column align="center" label="下载次数" prop="downloads" width="100"/>
    <el-table-column align="center" label="备注" prop="description">
      <template #default="scope">
        <el-popover
            :visible="scope.row.visible"
            :width="200"
            placement="bottom"
            trigger="manual">
          <div style="text-align: center">
            <span>{{ scope.row.name }}备注信息</span>
            <div style="margin: 5px auto">
              <el-input v-model="scope.row.description"
                        autosize
                        clearable
                        maxlength="220"
                        placeholder="请添加备注信息"
                        type="textarea"
              ></el-input>
            </div>
            <el-button size="small" @click="scope.row.visible=false">取消</el-button>
            <el-button size="small" @click="updateFile(scope.row)">保存</el-button>
          </div>
          <template #reference>
            <el-link :underline="false">
              <el-icon @click="scope.row.visible=true">
                <EditPen/>
              </el-icon>&nbsp;&nbsp;
            </el-link>
          </template>
        </el-popover>
        <span>{{ scope.row.description }}</span>
      </template>
    </el-table-column>
    <el-table-column align="center" label="操作">
      <template #default="scope">
        <el-button size="small" @click="downloadFile(scope.row.id)"
        >下载文件
        </el-button>
        <el-button
            size="small"
            type="danger"
            @click="delFileFun(scope.row)"
        >删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <pagination v-show="total>0" v-model:page="listQuery.page" v-model:size="listQuery.size" :total="total"
              @pagination="getTableData"/>

</template>

<script>
import {delFile, delManyFile, downloadManyFile, getDownloadUrl, getFile, updateFile} from "@/api/file";
import {diskSize, downloadFile, formatTime, getLocationOrigin, getRandomStr} from "@/utils";
import {ElMessage, ElMessageBox} from "element-plus";
import Pagination from "@/components/base/Pagination";
import {addShare} from "@/api/share";

const sortOptions = [
  {label: '上传时间 Ascending', key: 'created_at'},
  {label: '上传时间 Descending', key: '-created_at'},
  {label: '文件大小 Ascending', key: 'size'},
  {label: '文件大小 Descending', key: '-size'},
  {label: '下载次数 Ascending', key: 'downloads'},
  {label: '下载次数 Descending', key: '-downloads'}
]
export default {
  name: "FileManager",
  components: {
    Pagination
  },
  data() {
    const shortcuts = [
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
    ]
    const date = new Date()
    return {
      isLoading: false,
      shareVisible: false,
      tableData: [],
      selectedData: [],
      prefixUrl: getLocationOrigin(),
      total: 0,
      sortOptions,
      shortcuts,
      listQuery: {
        page: 1,
        size: 10,
        user_name: null,
        ordering: sortOptions[1].key,
        description: null
      }, formShare: {
        short: null,
        expired_time: date.getTime() + 3600 * 1000 * 24 * 7,
        password: '',
        description: '',
      }
    }
  }, methods: {
    showShareDialog() {
      if (this.selectedData && this.selectedData.length > 0) {
        this.formShare.short = null
        this.formShare.password = ''
        this.formShare.description = ''
        this.shareVisible = true
      } else {
        ElMessage.warning("请选择待分享的文件")
      }
    },
    makeRandomPwd() {
      this.formShare.password = getRandomStr(8)
    },
    getFileIdList() {
      let file_id_list = []
      this.selectedData.forEach(res => {
        file_id_list.push(res.file_id)
      })
      return file_id_list
    },
    downManyFileFun() {
      downloadManyFile(this.getFileIdList()).then(res => {
        res.data.forEach(url => {
          downloadFile(url)
        })
      })
    },
    shareManyFileFun() {
      addShare({file_id_list: this.getFileIdList(), share_info: this.formShare}).then(() => {
        ElMessage.success("操作成功")
        this.shareVisible = false
      }).catch(() => {
        this.shareVisible = false
      })
    },
    delManyFileFun() {
      ElMessageBox.confirm(
          `是否删除 ${this.selectedData.length} 个文件?`,
          'Warning',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消操作',
            type: 'warning',
          }
      ).then(() => {
        this.isLoading = true
        delManyFile(this.getFileIdList()).then(() => {
          ElMessage.success('删除成功')
          this.isLoading = false
          this.getTableData()
        }).catch(() => {
          this.isLoading = false
        })
      }).catch(() => {
        ElMessage({
          type: 'info',
          message: '取消操作',
        })
      })
    },
    handleSelectionChange(val) {
      this.selectedData = val
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getTableData()
    },
    updateFile(val) {
      this.isLoading = true
      updateFile(val).then(() => {
        this.isLoading = false
        val.visible = false
        ElMessage.success('操作成功')
      }).catch(() => {
        this.isLoading = false
      })

    },
    getTableData(refresh = false) {
      if (refresh) {
        this.listQuery.size = 10
        this.listQuery.page = 1
      }
      this.isLoading = true
      getFile(this.listQuery).then(res => {
        this.tableData = res.data.results
        this.total = res.data.count
        this.isLoading = false
      }).catch(() => {
        this.isLoading = false
      })
    }, sizeFormatter(row) {
      return diskSize(row.size)
    }, timeFormatter(row) {
      return formatTime(row.created_at)
    },
    delFileFun(row) {
      delFile(row.id).then(() => {
        ElMessage.success(`${row.name} 删除成功`)
        this.getTableData()
      })
    },
    downloadFile(id) {
      getDownloadUrl(id).then(res => {
        downloadFile(res.data.download_url)
      })
    },
  }, mounted() {
    this.getTableData(true)
  }
}
</script>

<style scoped>

</style>
