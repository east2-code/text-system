<template>
  <el-card>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom:10px;">
      <div>
        <el-input v-model="search" placeholder="搜索用户名/邮箱/公司-部门/授权码" style="width:260px;margin-right:10px;" @keyup.enter="loadData"/>
        <el-button type="primary" @click="loadData">搜索</el-button>
        <el-button @click="reset">重置</el-button>
      </div>
      <div>
        <el-button type="warning" @click="undoBatchDelete" :disabled="!undoList.length" style="margin-right:8px;">
          撤销删除
        </el-button>
        <el-button type="danger" @click="batchDelete" :disabled="!multipleSelection.length">批量删除</el-button>
        <el-button type="primary" @click="openDialog">新增授权</el-button>
      </div>
    </div>
    <el-table
      :data="pagedLicenses"
      highlight-current-row
      border
      ref="tableRef"
      @selection-change="onSelectionChange"
      style="margin-bottom:24px;"
      :row-class-name="rowClassName"
    >
      <el-table-column type="selection" width="50" />
      <el-table-column prop="username" label="用户名" min-width="100"/>
      <el-table-column prop="email" label="邮箱" min-width="120"/>
      <el-table-column prop="company" label="公司-部门" min-width="100"/>
      <el-table-column prop="software" label="软件" min-width="80"/>
      <el-table-column prop="license_key" label="授权码" min-width="220">
        <template #default="scope">
          <el-input
            v-model="scope.row.license_key"
            readonly
            size="small"
            style="width: 78%;"
            :title="scope.row.license_key"
          />
          <el-button size="small" @click="copy(scope.row.license_key)">复制</el-button>
        </template>
      </el-table-column>
      <el-table-column prop="expires_at" label="到期时间" min-width="140"/>
      <el-table-column prop="status" label="状态" min-width="100">
        <template #default="scope">
          <el-tag
            :type="tagType(scope.row.status)"
            effect="plain"
            size="small"
          >{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="250">
        <template #default="scope">
          <el-button size="small" @click="viewDetail(scope.row)">详情</el-button>
          <el-button size="small" type="info" @click="toggle(scope.row)">
            {{ scope.row.is_active ? "停用" : "启用" }}
          </el-button>
          <el-button size="small" type="success" @click="renew(scope.row)">续期</el-button>
          <el-popconfirm title="确定删除此授权？" @confirm="deleteLicense(scope.row)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
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
    <!-- 新增授权对话框 -->
    <el-dialog v-model="dialogVisible" title="新增授权" width="440px" :close-on-click-modal="false">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="105px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="公司-部门" prop="company">
          <el-input v-model="form.company" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="软件" prop="software_name">
          <el-select v-model="form.software_name" placeholder="请选择软件">
            <el-option
              v-for="soft in softwareList"
              :key="soft.id"
              :label="soft.name + ' ' + soft.version"
              :value="soft.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="硬件ID" prop="hardware_id">
          <el-input v-model="form.hardware_id" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="到期天数" prop="expiry_days">
          <el-input-number v-model="form.expiry_days" :min="1" :max="3650" style="width:100%"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="submitForm">保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const licenses = ref([])
const softwareList = ref([])
const search = ref('')
const page = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const form = ref({
  username: '', email: '', company: '',
  software_name: '', hardware_id: '', expiry_days: 365
})
const formRef = ref(null)
const tableRef = ref(null)
const multipleSelection = ref([])
const undoList = ref([])

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  software_name: [{ required: true, message: '请选择软件', trigger: 'change' }],
  hardware_id: [{ required: true, message: '请输入硬件ID', trigger: 'blur' }],
  expiry_days: [{ required: true, type: 'number', message: '请输入到期天数', trigger: 'blur' }]
}
const tagType = status => {
  if (status === "已停用") return "info"
  if (status === "已过期") return "danger"
  if (status === "即将到期") return "warning"
  return "success"
}
const rowClassName = ({ row }) => {
  if (row.status === "已停用") return 'row-disabled'
  if (row.status === "已过期") return 'row-expired'
  if (row.status === "即将到期") return 'row-expiring'
  return ''
}
const loadData = async () => {
  const res = await api.get('/all-licenses')
  if (res.code === 0) licenses.value = res.licenses
  const sw = await api.get('/software')
  if (sw.code === 0 && Array.isArray(sw.software)) softwareList.value = sw.software
}
const reset = () => {
  search.value = ''
  loadData()
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
    .then(() => ElMessage.success('已复制'))
    .catch(() => ElMessage.error('复制失败'))
}
const onSelectionChange = val => (multipleSelection.value = val)
const batchDelete = async () => {
  if (!multipleSelection.value.length) return
  if (!confirm(`确定删除选中的${multipleSelection.value.length}条授权？`)) return
  undoList.value = multipleSelection.value.map(x => x.id)
  for (const row of multipleSelection.value) {
    await api.delete(`/licenses/${row.id}`)
  }
  loadData()
}
const undoBatchDelete = async () => {
  if (!undoList.value.length) return
  await api.post('/licenses/undo-delete', { ids: undoList.value })
  undoList.value = []
  loadData()
}
const viewDetail = row => router.push(`/licenses/${row.id}`)
const deleteLicense = async row => {
  undoList.value = [row.id]
  await api.delete(`/licenses/${row.id}`)
  loadData()
}
const toggle = async row => {
  await api.patch(`/licenses/${row.id}/toggle`, { is_active: row.is_active ? 0 : 1 })
  loadData()
}
const renew = async row => {
  let days = prompt("请输入续期天数", "30")
  if (!days || isNaN(days)) return
  await api.patch(`/licenses/${row.id}/renew`, { add_days: Number(days) })
  loadData()
}
const submitForm = () => {
  formRef.value.validate(async valid => {
    if (!valid) return
    const res = await api.post('/licenses', form.value)
    if (res.license_key) {
      dialogVisible.value = false
      form.value = { username: '', email: '', company: '', software_name: '', hardware_id: '', expiry_days: 365 }
      loadData()
    }
  })
}
const openDialog = () => {
  form.value = { username: '', email: '', company: '', software_name: '', hardware_id: '', expiry_days: 365 }
  if (!softwareList.value.length) loadData()
  dialogVisible.value = true
}
onMounted(loadData)
</script>
<style scoped>
.row-expired { background: #ffeaea !important;}
.row-expiring { background: #fffbe6 !important;}
.row-disabled { background: #ececec !important; color:#aaa;}
</style>