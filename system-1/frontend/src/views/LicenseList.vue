<template>
  <el-card>
    <div class="top-bar">
      <div>
        <el-input v-model="search" :placeholder="$t('searchPlaceholder')" style="width:260px;margin-right:10px;" @keyup.enter="loadData"/>
        <el-button type="primary" @click="loadData">{{ $t('search') }}</el-button>
        <el-button @click="reset">{{ $t('reset') }}</el-button>
      </div>
      <div>
        <el-button type="success" @click="exportExcel">{{ $t('exportExcel') }}</el-button>
        <el-button type="primary" @click="dialogVisible=true">{{ $t('addLicense') }}</el-button>
        <el-button type="danger" :disabled="!multipleSelection.length" @click="batchDelete">{{ $t('batchDelete') }}</el-button>
        <el-button type="info" :disabled="!lastDeleted.length" @click="undoBatchDelete">{{ $t('undoBatchDelete') }}</el-button>
      </div>
    </div>
    <el-table
      ref="tableRef"
      :data="pagedLicenses"
      highlight-current-row
      border
      style="margin-bottom:24px;"
      @selection-change="handleSelectionChange"
      row-key="id"
    >
      <el-table-column type="selection" width="50" />
      <el-table-column prop="username" :label="$t('username')" min-width="100"/>
      <el-table-column prop="email" :label="$t('email')" min-width="120"/>
      <el-table-column prop="company" :label="$t('company')" min-width="100"/>
      <el-table-column prop="software" :label="$t('software')" min-width="80"/>
      <el-table-column prop="license_key" :label="$t('licenseKey')" min-width="220">
        <template #default="scope">
          <el-input v-model="scope.row.license_key" readonly size="small" style="width: 78%;" :title="scope.row.license_key"/>
          <el-button size="small" @click="copy(scope.row.license_key)">{{ $t('copy') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column prop="expires_at" :label="$t('expiresAt')" min-width="140"/>
      <el-table-column prop="status" :label="$t('status')" min-width="100">
        <template #default="scope">
          <el-tag :type="tagType(scope.row.status)" size="small" effect="plain">
            {{ $t('status_' + scope.row.statusKey) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" :label="$t('actions')" width="250">
        <template #default="scope">
          <el-button size="small" @click="viewDetail(scope.row)">{{ $t('detail') }}</el-button>
          <el-button size="small" type="info" @click="toggle(scope.row)">
            {{ scope.row.is_active ? $t('deactivate') : $t('activate') }}
          </el-button>
          <el-button size="small" type="success" @click="renew(scope.row)">{{ $t('renew') }}</el-button>
          <el-popconfirm :title="$t('deleteConfirm')" @confirm="deleteLicense(scope.row)">
            <template #reference>
              <el-button size="small" type="danger">{{ $t('delete') }}</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      :page-size="pageSize"
      :total="filteredLicenses.length"
      layout="total, prev, pager, next, sizes"
      :page-sizes="[5,10,20,50]"
      @size-change="handleSizeChange"
      style="text-align:right"
    />
  </el-card>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'
import { ElMessage } from 'element-plus'
import * as XLSX from 'xlsx'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const licenses = ref([])
const search = ref('')
const page = ref(1)
const pageSize = ref(10)
const multipleSelection = ref([])
const lastDeleted = ref([])

const tableRef = ref(null)

const statusMap = {
  "激活": "active",
  "已过期": "expired",
  "即将到期": "expiring",
  "已停用": "disabled"
}
const tagType = status => {
  switch (status) {
    case "已停用": return "info"
    case "已过期": return "danger"
    case "即将到期": return "warning"
    case "激活": return "success"
    default: return ""
  }
}
const loadData = async () => {
  const res = await api.get('/all-licenses')
  if (res.code === 0) {
    licenses.value = res.licenses.map(row => ({
      ...row,
      statusKey: statusMap[row.status] || "unknown"
    }))
  }
}
const filteredLicenses = computed(() =>
  licenses.value.filter(
    l =>
      l.username.includes(search.value) ||
      (l.email || '').includes(search.value) ||
      (l.company || '').includes(search.value) ||
      l.license_key.includes(search.value)
  )
)
const pagedLicenses = computed(() =>
  filteredLicenses.value.slice((page.value - 1) * pageSize.value, page.value * pageSize.value)
)
const handleSizeChange = val => (pageSize.value = val)
const copy = text => {
  navigator.clipboard.writeText(text)
    .then(() => ElMessage.success(t('copied')))
    .catch(() => ElMessage.error(t('copyFailed')))
}
const exportExcel = () => {
  const data = filteredLicenses.value.map(l => ({
    [t('username')]: l.username,
    [t('email')]: l.email,
    [t('company')]: l.company,
    [t('software')]: l.software,
    [t('licenseKey')]: l.license_key,
    [t('hardwareId')]: l.hardware_id,
    [t('expiresAt')]: l.expires_at,
    [t('status')]: t('status_' + l.statusKey)
  }))
  const ws = XLSX.utils.json_to_sheet(data)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Licenses')
  XLSX.writeFile(wb, 'licenses.xlsx')
}
const handleSelectionChange = (val) => {
  multipleSelection.value = val
}
const batchDelete = async () => {
  const ids = multipleSelection.value.map(item => item.id)
  if (!ids.length) return
  // 真实请求
  const res = await api.post('/batch-delete-licenses', { ids })
  if (res.code === 0) {
    lastDeleted.value = multipleSelection.value
    loadData()
    ElMessage.success(t('batchDeleteSuccess') || '批量删除成功')
    multipleSelection.value = []
    tableRef.value.clearSelection()
  }
}
const undoBatchDelete = async () => {
  if (!lastDeleted.value.length) return
  const ids = lastDeleted.value.map(item => item.id)
  const res = await api.post('/undo-batch-delete-licenses', { ids })
  if (res.code === 0) {
    loadData()
    ElMessage.success(t('undoBatchDeleteSuccess') || '撤销批量删除成功')
    lastDeleted.value = []
  }
}
onMounted(loadData)
</script>
<style scoped>
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom:10px;
}
.el-table .el-table__row:hover {
  transition: background 0.2s;
  background: #eaf6ff !important;
}
.el-button {
  transition: box-shadow .18s,background .18s;
}
.el-button:hover {
  box-shadow: 0 2px 12px #409eff33;
  background: #e3f0ff !important;
}
</style>