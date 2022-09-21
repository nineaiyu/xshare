<template>
  <div class="filter-container">
    <el-input v-model="listQuery.short" class="filter-item" clearable placeholder="分享短连接" style="width: 140px;"
              @keyup.enter="handleFilter"/>
    <el-input v-model="listQuery.description" class="filter-item" clearable placeholder="备注" style="width: 140px;"
              @keyup.enter="handleFilter"/>
    <el-select v-model="listQuery.ordering" class="filter-item" style="width: 180px" @change="handleFilter">
      <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key"/>
    </el-select>

    <el-select v-model="listQuery.expired" class="filter-item" clearable style="width: 180px" @change="handleFilter">
      <el-option v-for="item in expiredOptions" :key="item.key" :label="item.label" :value="item.key"/>
    </el-select>

    <el-button class="filter-item" icon="Search" plain type="primary" @click="handleFilter">
      搜索&nbsp;&nbsp;&nbsp;
    </el-button>

    <div style="float: right">
      <el-button class="filter-item" icon="Delete" plain type="danger" @click="delManyShareFun">
        删除选中分享&nbsp;&nbsp;&nbsp;
      </el-button>
    </div>
  </div>
  <el-table
      v-loading="isLoading"
      :data="tableData"
      :row-class-name="tableRowClassName"
      border
      @selection-change="handleSelectionChange"
  >
    <el-table-column align="center" type="selection" width="55"/>
    <el-table-column align="center" label="文件列表" type="expand" width="55">
      <template #default="props">
        <div style="width: 96%;text-align: center;float: right">
          <el-table :data="props.row.file_info_list" border stripe>
            <el-table-column type="index"/>
            <el-table-column align="center" label="文件名" prop="name">
              <template #default="scope">
                <el-link :underline="false">{{ scope.row.name }}</el-link>
              </template>
            </el-table-column>
            <el-table-column :formatter="sizeFormatter" align="center" label="文件大小" prop="size" width="90"/>

            <el-table-column :formatter="uptimeFormatter" align="center" label="上传时间" prop="created_at"/>
            <el-table-column align="center" label="下载次数" prop="downloads" width="100"/>
            <el-table-column align="center" label="备注" prop="description"/>
            <el-table-column align="center" label="操作" width="100">
              <template #default="scope">
                <el-button size="small" @click="downloadFile(scope.row.id)">下载文件</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </el-table-column>
    <el-table-column align="center" label="短连接" prop="short" width="100">
      <template #default="scope">
        <el-popover v-if="!scope.row.is_expired"
                    :width="200"
                    placement="top-start"
                    trigger="hover">
          <template #reference>
            <el-link :underline="false"
                     @click="$router.push({name:'short',params :{short:scope.row.short},query:{password:scope.row.password}})">
              {{ scope.row.short }}
            </el-link>
          </template>
          点击跳转下载页或
          <el-link :underline='false'
                   @click="handleCopy(`${makeShortUrl(scope.row.short)}?password=${scope.row.password}`,$event)"><span
              style="color: teal">复制</span></el-link>
          下载页连接
        </el-popover>
        <el-tooltip v-else placement="top">
          <template #content>
            分享已过期
          </template>
          <span>{{ scope.row.short }}</span>
        </el-tooltip>
      </template>
    </el-table-column>
    <el-table-column :formatter="sizeFormatter" align="center" label="大小" prop="total_size" width="90"/>
    <el-table-column align="center" label="文件数量" prop="count" width="60"/>
    <el-table-column :formatter="timeFormatter" align="center" label="分享时间" prop="created_time"/>
    <el-table-column :formatter="expireTimeFormatter" align="center" label="过期时间" prop="expired_time">
      <template #default="scope">
        <el-popover
            :visible="scope.row.timeVisible"
            :width="300"
            placement="bottom"
            trigger="manual">
          <div style="text-align: center">
            <span>{{ scope.row.name }}过期时间</span>
            <div style="margin: 5px auto">
              <el-date-picker
                  v-model="scope.row.expired_time"
                  format="YYYY/MM/DD hh:mm:ss"
                  placeholder="请选择过期时间"
                  type="datetime"
                  @change="updateShare(scope.row)"
              />
            </div>
            <el-button size="small" @click="scope.row.timeVisible=false">取消</el-button>
            <el-button size="small" @click="updateShare(scope.row)">保存</el-button>
          </div>
          <template #reference>
            <el-link :underline="false" @click="scope.row.timeVisible=true">
              <span>{{ formatTime(scope.row.expired_time) }}</span>
            </el-link>
          </template>
        </el-popover>
      </template>
    </el-table-column>
    <el-table-column align="center" label="访问密码" prop="password">
      <template #default="scope">
        <el-popover
            :visible="scope.row.pwdVisible"
            :width="200"
            placement="bottom"
            trigger="manual">
          <div style="text-align: center">
            <span>{{ scope.row.name }}访问密码</span>
            <div style="margin: 5px auto">
              <el-input v-model="scope.row.password"
                        clearable
                        maxlength="16"
                        placeholder="请添加访问密码"
                        show-word-limit
              ></el-input>
            </div>
            <el-button size="small" @click="scope.row.pwdVisible=false">取消</el-button>
            <el-button size="small" @click="updateShare(scope.row)">保存</el-button>
          </div>
          <template #reference>
            <el-link :underline="false">
              <el-icon @click="scope.row.pwdVisible=true">
                <EditPen/>
              </el-icon>&nbsp;&nbsp;
            </el-link>
          </template>
        </el-popover>
        <el-tooltip placement="top">
          <template #content>
            点击复制密码
          </template>
          <span @click="handleCopy(scope.row.password,$event)">{{ scope.row.password }}</span>
        </el-tooltip>
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
            <el-button size="small" @click="updateShare(scope.row)">保存</el-button>
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
        <el-button size="small" @click="downloadShare(scope.row)"
        >下载文件
        </el-button>
        <el-button
            size="small"
            type="danger"
            @click="delShareFun(scope.row)"
        >删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <pagination v-show="total>0" v-model:page="listQuery.page" v-model:size="listQuery.size" :total="total"
              @pagination="getTableData"/>

</template>

<script>
import clip from '@/utils/clipboard'
import {diskSize, downloadFile, formatTime, getLocationOrigin} from "@/utils";
import {ElMessage, ElMessageBox} from "element-plus";
import Pagination from "@/components/base/Pagination";
import {delManyShare, delShare, getShare, updateShare} from "@/api/share";
import {downloadManyFile, getDownloadUrl} from "@/api/file";

const sortOptions = [
  {label: '创建时间 Ascending', key: 'created_time'},
  {label: '创建时间 Descending', key: '-created_time'},
  {label: '过期时间 Ascending', key: 'expired_time'},
  {label: '过期时间 Descending', key: '-expired_time'},
]
const expiredOptions = [
  {label: '已经过期', key: true},
  {label: '还未过期', key: false},
]
export default {
  name: "FileShare",
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
      expiredOptions,
      listQuery: {
        page: 1,
        size: 10,
        user_name: null,
        ordering: sortOptions[1].key,
        description: null,
        expired: null
      }
    }
  }, methods: {
    handleCopy(text, event) {
      clip(text, event)
    },
    makeShortUrl(short) {
      return getLocationOrigin() + short
    },
    formatTime,
    getShareIdList() {
      let share_id_list = []
      this.selectedData.forEach(res => {
        share_id_list.push(res.short)
      })
      return share_id_list
    },
    delManyShareFun() {
      ElMessageBox.confirm(
          `是否删除 ${this.selectedData.length} 条分享记录?`,
          'Warning',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消操作',
            type: 'warning',
          }
      ).then(() => {
        this.isLoading = true
        delManyShare(this.getShareIdList()).then(() => {
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
    downloadFile(id) {
      getDownloadUrl(id).then(res => {
        console.log(res)
        downloadFile(res.data.download_url)
      })
    },
    getFileIdList(row) {
      let file_id_list = []
      row.file_info_list.forEach(res => {
        file_id_list.push(res.file_id)
      })
      return file_id_list
    },
    downloadShare(row) {
      downloadManyFile(this.getFileIdList(row)).then(res => {
        res.data.forEach(url => {
          downloadFile(url.download_url)
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
    updateShare(val) {
      this.isLoading = true
      updateShare(val).then(() => {
        this.isLoading = false
        val.visible = false
        val.pwdVisible = false
        val.timeVisible = false
        ElMessage.success('操作成功')
        this.getTableData()
      })

    },
    getTableData(refresh = false) {
      if (refresh) {
        this.listQuery.size = 10
        this.listQuery.page = 1
      }
      this.isLoading = true
      getShare(this.listQuery).then(res => {
        this.tableData = res.data.results
        this.total = res.data.count
        this.isLoading = false
      })
      // eslint-disable-next-line no-unused-vars
    }, tableRowClassName({row, rowIndex}) {
      if (row.is_expired) {
        return 'warning-row'
      }
      return 'success-row'
    }, uptimeFormatter(row) {
      return formatTime(row.created_at)
    }, timeFormatter(row) {
      return formatTime(row.created_time)
    }, expireTimeFormatter(row) {
      return formatTime(row.expired_time)
    }, sizeFormatter(row) {
      return diskSize(row.size)
    },
    delShareFun(row) {
      delShare(row.id).then(() => {
        ElMessage.success(`${row.short} 删除成功`)
        this.getTableData()
      })
    },
  }, mounted() {
    this.getTableData(true)
  }
}
</script>

<style scoped>

</style>
