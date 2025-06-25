<template>
  <el-card>
    <h3 style="margin:0 0 16px 0;">软件管理</h3>
    <el-form :model="form" inline label-width="60px" :rules="rules" ref="formRef" style="margin-bottom:18px;">
      <el-form-item label="名称" prop="name"><el-input v-model="form.name"/></el-form-item>
      <el-form-item label="版本" prop="version"><el-input v-model="form.version"/></el-form-item>
      <el-form-item>
        <el-button type="primary" @click="addSoftware">新增</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="softwareList" border>
      <el-table-column prop="name" label="名称" min-width="120"/>
      <el-table-column prop="version" label="版本" min-width="120"/>
      <el-table-column fixed="right" width="100">
        <template #default="scope">
          <el-popconfirm title="确定删除此软件？" @confirm="deleteSoftware(scope.row)">
            <template #reference>
              <el-button type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const softwareList = ref([])
const form = ref({ name: '', version: '' })
const formRef = ref(null)
const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  version: [{ required: true, message: '请输入版本', trigger: 'blur' }]
}
const loadList = async () => {
  const res = await api.get('/software')
  if (res.software) softwareList.value = res.software
}
const addSoftware = () => {
  formRef.value.validate(async valid => {
    if (!valid) return
    await api.post('/software', form.value)
    form.value = { name: '', version: '' }
    loadList()
  })
}
const deleteSoftware = async row => {
  await api.delete(`/software/${row.id}`)
  loadList()
}
onMounted(loadList)
</script>