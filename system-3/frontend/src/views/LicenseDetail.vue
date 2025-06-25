<template>
  <el-card v-if="license">
    <h3>授权详情</h3>
    <el-descriptions :column="2" border>
      <el-descriptions-item label="用户名">{{ license.username }}</el-descriptions-item>
      <el-descriptions-item label="邮箱">{{ license.email || '未提供' }}</el-descriptions-item>
      <el-descriptions-item label="公司">{{ license.company || '未提供' }}</el-descriptions-item>
      <el-descriptions-item label="软件">{{ license.software }}</el-descriptions-item>
      <el-descriptions-item label="硬件ID">{{ license.hardware_id }}</el-descriptions-item>
      <el-descriptions-item label="授权码">
        <el-input v-model="license.license_key" readonly size="small" style="width: 85%;" />
        <el-button size="small" @click="copy(license.license_key)">复制</el-button>
      </el-descriptions-item>
      <el-descriptions-item label="到期时间">{{ license.expires_at }}</el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="tagType">{{ statusText }}</el-tag>
      </el-descriptions-item>
    </el-descriptions>
    <el-button type="primary" @click="$router.back()" style="margin-top:24px;">返回</el-button>
  </el-card>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const license = ref(null)
const copy = text => {
  navigator.clipboard.writeText(text)
    .then(() => ElMessage.success('已复制'))
    .catch(() => ElMessage.error('复制失败'))
}
const fetchDetail = async () => {
  const res = await api.get(`/license-detail/${route.params.id}`)
  if (res.id) license.value = res
}
const statusText = computed(() => {
  if (!license.value) return ''
  const now = new Date()
  const expire = new Date(license.value.expires_at)
  if (expire < now) return '已过期'
  if (!license.value.is_active) return '已停用'
  return '激活'
})
const tagType = computed(() => {
  if (!license.value) return ''
  const now = new Date()
  const expire = new Date(license.value.expires_at)
  if (expire < now) return 'danger'
  if (!license.value.is_active) return 'info'
  return 'success'
})
onMounted(fetchDetail)
</script>