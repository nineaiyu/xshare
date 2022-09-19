<template>
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
    </div>
  </div>
  <el-table
      v-loading="isLoading"
      :data="tableData"
      :row-class-name="tableRowClassName"
      border
      style="width: 100%"
      @selection-change="handleSelectionChange"
  >
    <el-table-column align="center" type="selection" width="55"/>
    <el-table-column align="center" label="文件名" prop="name"/>
    <el-table-column :formatter="sizeormatter" align="center" label="文件大小" prop="size" width="90"/>
    <el-table-column :formatter="timeFormatter" align="center" label="上传时间" prop="created_at" width="100"/>
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
            <el-link>
              <el-icon @click="scope.row.visible=true">
                <EditPen/>
              </el-icon>
            </el-link>
          </template>
        </el-popover>
        <span>{{ scope.row.description }}</span>
      </template>
    </el-table-column>
    <el-table-column align="center" label="操作" width="90">
      <template #default="scope">
        <div style="display: flex;flex-direction: column;justify-content: space-around;align-items:center;height: 60px">
          <el-button size="small" @click="downloadFile(scope.row.id)"
          >下载文件
          </el-button>
          <el-button
              size="small"
              type="danger"
              @click="delFileFun(scope.row)"
          >删除
          </el-button>
        </div>

      </template>
    </el-table-column>
  </el-table>
  <pagination v-show="total>0" v-model:page="listQuery.page" v-model:size="listQuery.size" :total="total"
              @pagination="getTableData"/>

</template>

<script>
import {delFile, delManyFile, downloadManyFile, getFile, updateFile} from "@/api/file";
import {diskSize, downloadFile, formatTime} from "@/utils";
import {ElMessage, ElMessageBox} from "element-plus";
import Pagination from "@/components/base/Pagination";
import {getDownloadUrl} from "@/api/download";

const sortOptions = [
  {label: '上传时间 Ascending', key: 'created_at'},
  {label: '上传时间 Descending', key: '-created_at'},
  {label: '文件大小 Ascending', key: 'size'},
  {label: '文件大小 Descending', key: '-size'},
  {label: '下载次数 Ascending', key: 'downloads'},
  {label: '下载次数 Descending', key: '-downloads'}
]
export default {
  name: "FileLobby",
  components: {
    Pagination
  },
  data() {
    return {
      isLoading: false,
      tableData: [],
      selectedData: [],
      total: 0,
      sortOptions,
      listQuery: {
        page: 1,
        size: 10,
        user_name: null,
        ordering: sortOptions[1].key,
        description: null
      }
    }
  }, methods: {
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
      console.log(val)
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
      })

    },
    stopLoop() {
      this.loop = false
      this.sid = ''
      this.qrcode = ''
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
      })
    }, tableRowClassName(row) {
      if (!row.active || row.enable) {
        return 'warning-row'
      }
    }, sizeormatter(row) {
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
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}

.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
