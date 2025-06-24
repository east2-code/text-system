<template>
  <el-card>
    <div class="top-bar">
      <div>
        <el-input v-model="search" :placeholder="$t('software')" style="width:180px;margin-right:10px;" @keyup.enter="loadData"/>
        <el-button type="primary" @click="loadData">{{ $t('search') }}</el-button>
        <el-button @click="reset">{{ $t('reset') }}</el-button>
      </div>
      <div>
        <el-button type="success" @click="exportExcel">{{ $t('exportExcel') }}</el-button>
        <el-button type="primary" @click="dialogVisible=true">{{ $t('addSoftware') }}</el-button>
        <el-button type="danger" :disabled="!multipleSelection.length" @click="batchDelete">{{ $t('batchDelete') }}</el-button>
        <el-button type="info" :disabled="!lastDeleted.length" @click="undoBatchDelete">{{ $t('undoBatchDelete') }}</el-button>
      </div>
    </div>
    <el-table
      ref="tableRef"
      :data="pageData"
      highlight-current-row
      border
      @selection-change="handleSelectionChange"
      row-key="id"
    >
      <el-table-column type="selection" width="50"/>
      <el-table-column prop="name" :label="$t('software')" min-width="120"/>
      <el-table-column prop="version" :label="$t('version')" min-width="100"/>
      <el-table-column fixed="right" :label="$t('actions')" width="140">
        <template #default="scope">
          <!-- 编辑和删除按钮略 -->
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      :page-size="pageSize"
      :total="filteredData.length"
      layout="total, prev, pager, next, sizes"
      :page-sizes="[5,10,20,50]"
      @size-change="val=>pageSize=val"
      style="text-align:right"
    />
  </el-card>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'
import * as XLSX from 'xlsx'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const data = ref([])
const search = ref('')
const page = ref(1)
const pageSize = ref(10)
const multipleSelection = ref([])
const lastDeleted = ref([])
const tableRef = ref(null)
const filteredData = computed(() =>
  data.value.filter(
    l =>
      (l.name || '').includes(search.value) ||
      (l.version || '').includes(search.value)
  )
)
const pageData = computed(() =>
  filteredData.value.slice((page.value - 1) * pageSize.value, page.value * pageSize.value)
)
const loadData = async () => {
  const res = await api.get('/software')
  if (res.code === 0) data.value = res.software
}
const exportExcel = () => {
  const exl = filteredData.value.map(l => ({
    [t('software')]: l.name,
    [t('version')]: l.version
  }))
  const ws = XLSX.utils.json_to_sheet(exl)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Software')
  XLSX.writeFile(wb, 'software.xlsx')
}
const handleSelectionChange = (val) => {
  multipleSelection.value = val
}
const batchDelete = async () => {
  const ids = multipleSelection.value.map(item => item.id)
  if (!ids.length) return
  const res = await api.post('/batch-delete-software', { ids })
  if (res.code === 0) {
    lastDeleted.value = multipleSelection.value
    loadData()
    ElMessage.success(t('batchDeleteSuccess'))
    multipleSelection.value = []
    tableRef.value.clearSelection()
  }
}
const undoBatchDelete = async () => {
  if (!lastDeleted.value.length) return
  const ids = lastDeleted.value.map(item => item.id)
  const res = await api.post('/undo-batch-delete-software', { ids })
  if (res.code === 0) {
    loadData()
    ElMessage.success(t('undoBatchDeleteSuccess'))
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