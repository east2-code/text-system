<template>
  <el-row :gutter="26" style="margin-bottom:38px;">
    <el-col :span="6">
      <el-card class="stat-card glassy" :class="'card1'" shadow="hover">
        <div class="stat-label">{{ $t('totalLicenses') }}</div>
        <div class="stat-value">{{ stats.total }}</div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card glassy" :class="'card2'" shadow="hover">
        <div class="stat-label">{{ $t('expiringSoon') }}</div>
        <div class="stat-value">{{ stats.expiring }}</div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card glassy" :class="'card3'" shadow="hover">
        <div class="stat-label">{{ $t('expired') }}</div>
        <div class="stat-value">{{ stats.expired }}</div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card glassy" :class="'card4'" shadow="hover">
        <div class="stat-label">{{ $t('activeLicenses') }}</div>
        <div class="stat-value">{{ stats.active }}</div>
      </el-card>
    </el-col>
  </el-row>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
const stats = ref({ total: 0, expiring: 0, expired: 0, active: 0 })
onMounted(async () => {
  const statRes = await api.get('/stats')
  if (statRes.code === 0) stats.value = statRes.data
})
</script>
<style scoped>
.stat-card {
  border-radius: 18px;
  min-height: 120px;
  box-shadow: var(--card-shadow);
  transition: box-shadow .25s,transform .2s;
  cursor: pointer;
  background: var(--card-bg);
}
.card1 { background: linear-gradient(120deg,#bae6fd 0%,#f0faff 100%);}
.card2 { background: linear-gradient(120deg,#fff7e6 0%,#fff3e0 100%);}
.card3 { background: linear-gradient(120deg,#ffe0e6 0%,#fff0f0 100%);}
.card4 { background: linear-gradient(120deg,#e4ffd7 0%,#fafff7 100%);}
.stat-card:hover {
  box-shadow: 0 8px 36px #409eff30;
  transform: translateY(-6px) scale(1.035);
  background: var(--card-hover) !important;
}
.stat-label {
  font-weight: bold;
  font-size: 1.09em;
  color: #409EFF;
  margin-bottom: 16px;
  letter-spacing:1.2px;
}
.stat-value {
  font-size: 2.4em;
  font-weight: bold;
  color: #1a202c;
  text-shadow: 0 2px 12px #fff6;
  letter-spacing:2.5px;
}
</style>