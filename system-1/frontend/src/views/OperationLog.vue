<template>
  <el-card>
    <div style="display: flex; justify-content: flex-end; margin-bottom:10px;">
      <el-button type="success" @click="exportExcel">{{ $t('exportExcel') }}</el-button>
    </div>
    <el-table :data="logs" border>
      <el-table-column prop="time" :label="$t('time')" width="160"/>
      <el-table-column prop="user" :label="$t('user')" width="110"/>
      <el-table-column prop="action" :label="$t('action')" width="140"/>
      <el-table-column prop="detail" :label="$t('detail')"/>
    </el-table>
  </el-card>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import * as XLSX from 'xlsx'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const logs = ref([])
const loadLogs = async () => {
  const res = await api.get('/logs?limit=100')
  if (res.code === 0) logs.value = res.logs
}
const exportExcel = () => {
  const data = logs.value.map(l => ({
    [t('time')]: l.time,
    [t('user')]: l.user,
    [t('action')]: l.action,
    [t('detail')]: l.detail
  }))
  const ws = XLSX.utils.json_to_sheet(data)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Logs')
  XLSX.writeFile(wb, 'operation_logs.xlsx')
}
onMounted(loadLogs)
</script>