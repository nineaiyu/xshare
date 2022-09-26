<template>
  <div class="filter-container">
    <el-input v-model="listQuery.user_name" class="filter-item" clearable placeholder="用户名" style="width: 140px;"
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
      <el-popover
          :visible="sid!==''"
          :width="200"
          placement="bottom"
          trigger="manual">
        <div style="text-align: center">
          <span>手机阿里云盘扫码授权</span>
          <vue-qr v-if="qrcode" :text="qrcode" style="width: 176px;height: 166px"></vue-qr>
          <el-button size="small" @click="stopLoop">退出</el-button>
        </div>
        <template #reference>
          <el-button class="filter-item"
                     icon="DocumentAdd"
                     plain type="primary" @click="addDrive('添加')">添加阿里云盘授权&nbsp;&nbsp;&nbsp;
          </el-button>
        </template>

      </el-popover>
    </div>
  </div>
  <el-table
      v-loading="isLoading"
      :data="tableData"
      :row-class-name="tableRowClassName"
      border
      style="width: 100%"
  >
    <el-table-column align="center" label="用户名" prop="user_name" width="100"/>
    <el-table-column align="center" label="头像" prop="头像" width="120">
      <template #default="scope">
        <el-image :src="scope.row.avatar"></el-image>
      </template>
    </el-table-column>
    <el-table-column :formatter="totalFormatter" align="center" label="磁盘总大小" prop="total_size" width="100"/>
    <el-table-column :formatter="usedFormatter" align="center" label="已使用" prop="used_size" width="100"/>
    <el-table-column :formatter="timeFormatter" align="center" label="添加时间" prop="created_time" width="100"/>
    <el-table-column align="center" label="是否启用" prop="enable" width="65">
      <template #default="scope">
        <el-switch
            v-model="scope.row.enable"
            active-icon="Check"
            class="mt-2"
            inactive-icon="Close"
            inline-prompt
            @change="updateDrive(scope.row)"
        />
      </template>

    </el-table-column>
    <el-table-column align="center" label="是否激活" prop="active" width="90">
      <template #default="scope">
        <el-tag v-if="scope.row.active">已激活</el-tag>
        <el-tag v-else type="danger" @click="addDrive('激活')">待激活</el-tag>
      </template>
    </el-table-column>
    <el-table-column align="center" label="是否私有" prop="private" width="65">
      <template #default="scope">
        <el-switch
            v-model="scope.row.private"
            active-icon="Check"
            class="mt-2"
            inactive-icon="Close"
            inline-prompt
            @change="updateDrive(scope.row)"
        />
      </template>
    </el-table-column>
    <el-table-column align="center" label="备注" prop="description">
      <template #default="scope">
        <el-popover
            :visible="scope.row.visible"
            :width="200"
            placement="bottom"
            trigger="manual">
          <div style="text-align: center">
            <span>{{ scope.row.user_name }}备注信息</span>
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
            <el-button size="small" @click="updateDrive(scope.row)">保存</el-button>
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
    <el-table-column align="center" label="操作" width="90">
      <template #default="scope" >
        <div style="display: flex;justify-content: space-around;flex-direction: column;height: 100px">
        <el-row>
          <el-button size="small" @click="addDrive('更新')">更新授权</el-button>
        </el-row>
        <el-row>
          <el-button size="small" @click="cleanDrive(scope.row)">清理空间</el-button>
        </el-row>
        <el-row>
          <el-button size="small" type="danger" @click="delStorage(scope.row)">删除空间</el-button>
        </el-row>
        </div>

      </template>
    </el-table-column>
  </el-table>
  <pagination v-show="total>0" v-model:page="listQuery.page" v-model:size="listQuery.size" :total="total"
              @pagination="getTableData"/>

</template>

<script>
import {checkQrDrive, delDrive, getDrive, getQrDrive, operateDrive, updateDrive} from "@/api/drive";
import {diskSize, formatTime} from "@/utils";
import vueQr from 'vue-qr/src/packages/vue-qr.vue'
import {ElMessage, ElMessageBox} from "element-plus";
import Pagination from "@/components/base/Pagination";

const sortOptions = [
  {label: '更新时间 Ascending', key: 'updated_time'},
  {label: '更新时间 Descending', key: '-updated_time'},
  {label: '创建时间 Ascending', key: 'created_time'},
  {label: '创建时间 Descending', key: '-created_time'},
  {label: '使用空间 Ascending', key: 'used_size'},
  {label: '使用空间 Descending', key: '-used_size'},
  {label: '总空间 Ascending', key: 'total_size'},
  {label: '总空间 Descending', key: '-total_size'}
]
export default {
  name: "AliDrive",

  components: {
    vueQr,
    Pagination
  },
  data() {
    return {
      isLoading: false,
      tableData: [],
      qrcode: '',
      sid: '',
      loop: true,
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
    cleanDrive(row) {
      this.isLoading = true
      operateDrive({pk: row.id, action: 'clean'}).then(() => {
        ElMessage.success('空间清理完成')
        this.isLoading = false
      }).catch(() => {
        this.isLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getTableData()
    },
    updateDrive(val) {
      this.isLoading = true
      updateDrive(val).then(() => {
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
      getDrive(this.listQuery).then(res => {
        this.tableData = res.data.results
        this.total = res.data.count
        this.isLoading = false
      })
      // eslint-disable-next-line no-unused-vars
    }, tableRowClassName({row, index}) {
      if (row.active && row.enable) {
        return 'success-row'
      } else if (row.enable && !row.active) {
        return 'warning-row'
      } else
        return ''
    }, totalFormatter(row) {
      return diskSize(row.total_size)
    }, usedFormatter(row) {
      return diskSize(row.used_size)
    }, timeFormatter(row) {
      return formatTime(row.created_time)
    },
    addDrive(title) {
      getQrDrive().then(res => {
        this.qrcode = res.data.qr_link
        this.sid = res.data.sid
        this.loop = true
        this.loopCheckScan(title)
      })
    },
    delStorage(row) {
      ElMessageBox.confirm(
          `是否删除 ${row.user_name} 授权? 删除该授权，同时也会清理该云盘数据`,
          'Warning',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消操作',
            type: 'warning',
          }
      ).then(() => {
        this.isLoading = true
        delDrive(row.id).then(() => {
          ElMessage.success('删除成功')
          this.getTableData()
          this.isLoading = false
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
    loopCheckScan(title) {
      if (this.loop) {
        checkQrDrive({sid: this.sid}).then(res => {
          if (res.data.pending_status) {
            if (res.data.data.msg) {
              ElMessage.success(title + "授权失败，" + res.data.data.msg)
            } else {
              ElMessage.success(title + "授权成功")
            }
            this.stopLoop()
            this.getTableData()
          } else {
            this.loopCheckScan(title)
          }
        })
      }
    }
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
