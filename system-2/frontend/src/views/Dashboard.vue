<template>
  <div>
    <el-row :gutter="22" style="margin-bottom:32px">
      <el-col :span="8">
        <el-card class="stat-card glassy">
          <div>总授权数</div>
          <div class="stat-value">{{ stats.total }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card glassy">
          <div>即将到期(30天内)</div>
          <div class="stat-value" style="color:#ff9800;">{{ stats.expiring }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card glassy">
          <div>已过期</div>
          <div class="stat-value" style="color:#f44336;">{{ stats.expired }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-alert type="info" title="欢迎使用授权管理系统！" show-icon />
    <div class="dashboard-desc">
      <p>本系统支持授权管理、软件管理、到期提醒等功能。</p>
      <p>如遇问题请联系管理员。</p>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const stats = ref({ total: 0, expiring: 0, expired: 0 })
onMounted(async () => {
  const res = await api.get('/stats')
  if (res.code === 0) stats.value = res.data
})
</script>
<style scoped>
.stat-card {
  text-align: center;
  font-size: 1.1em;
  background: rgba(255,255,255,0.22);
  border-radius: 18px;
  border: none;
  box-shadow: 0 6px 24px #409EFF22, 0 1.5px 1.5px #409EFF11;
}
.glassy {
  background: rgba(255,255,255,0.22);
  backdrop-filter: blur(7px) saturate(150%);
  border: 1px solid rgba(255,255,255,0.12);
}
.stat-value {
  font-size: 2.7em;
  font-weight: bold;
  color: #409EFF;
  margin: 13px 0 0 0;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 12px #409EFF44;
}
.dashboard-desc {
  margin-top:34px;
  color:#666;
  font-size: 1.13em;
  text-shadow: 0 1px 10px #409EFF11;
  background: rgba(255,255,255,0.16);
  border-radius: 8px;
  padding: 18px 22px;
  max-width: 560px;
  box-shadow: 0 2px 16px #409EFF12;
}
</style>