<template>
  <el-container style="height: 100vh;">
    <el-aside width="212px" class="sidebar">
      <div class="logo-bar">
        <img src="https://cdn.jsdelivr.net/gh/east2-code/pic-repo/img/logo-cube-blue.svg" class="logo-img" />
        <span>授权管理系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="var(--menu-bg)"
        text-color="var(--menu-text)"
        active-text-color="var(--menu-active)"
        style="border-right:none"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/software">
          <el-icon><Monitor /></el-icon>
          <span>软件管理</span>
        </el-menu-item>
        <el-menu-item index="/licenses">
          <el-icon><Memo /></el-icon>
          <span>授权管理</span>
        </el-menu-item>
        <el-menu-item @click="logout">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </el-menu-item>
      </el-menu>
      <div style="text-align:center; margin-top:26px;">
        <el-select v-model="themeVal" @change="toggleTheme" style="width:100px;">
          <el-option label="亮色" value="light" />
          <el-option label="夜间" value="dark" />
          <el-option label="极简" value="minimal" />
          <el-option label="炫彩" value="colorful" />
        </el-select>
      </div>
    </el-aside>
    <el-container>
      <el-header class="header-bar">
        <div style="display:flex;align-items:center;gap:7px;">
          <el-icon color="#409EFF"><HomeFilled v-if="activeMenu==='/'" /></el-icon>
          <el-icon color="#409EFF"><Memo v-if="activeMenu==='/licenses'" /></el-icon>
          <el-icon color="#409EFF"><Monitor v-if="activeMenu==='/software'" /></el-icon>
          <span class="nav-title">{{ pageTitle }}</span>
        </div>
        <div class="header-user">
          <el-avatar size="medium" style="background:#409EFF;">A</el-avatar>
          <span style="margin-left:10px; color:#409EFF;font-weight:bold;">管理员</span>
        </div>
      </el-header>
      <el-main class="main-area">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed, ref } from 'vue'
import { HomeFilled, Memo, Monitor, SwitchButton } from '@element-plus/icons-vue'
import { theme } from '../theme'

const route = useRoute()
const router = useRouter()
const activeMenu = computed(() => {
  if (route.path.startsWith('/licenses')) return '/licenses'
  if (route.path.startsWith('/software')) return '/software'
  return route.path
})
const pageTitle = computed(() => {
  switch (activeMenu.value) {
    case '/licenses': return '授权管理'
    case '/software': return '软件管理'
    case '/': return '仪表盘'
    default: return ''
  }
})
const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
const themeVal = ref(theme.value)
const toggleTheme = val => {
  theme.value = val
  themeVal.value = val
}
</script>
<style scoped>
.sidebar {
  background: var(--menu-bg);
  color: var(--menu-text);
  box-shadow: 2px 0 15px #409EFF11;
  transition: background 0.3s;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding-top: 0;
}
.logo-bar {
  height: 70px;
  display: flex;
  align-items: center;
  font-size: 1.23em;
  font-weight: bold;
  padding-left: 18px;
  margin-bottom: 13px;
  border-bottom: 1px solid #1e2636;
  gap: 13px;
  letter-spacing: 2px;
  color: #fff;
  text-shadow: 0 2px 16px #409EFF50;
  user-select: none;
}
.logo-img {
  height: 38px;
  margin-right: 7px;
  filter: drop-shadow(0 0 11px #409EFF88);
}
.header-bar {
  background: linear-gradient(90deg,#409EFF22 0px,#fff 80%);
  display: flex;
  align-items: center;
  height: 62px;
  justify-content: space-between;
  box-shadow: 0 2px 20px #409EFF22;
  border-bottom: 2px solid #409EFF11;
  z-index:10;
}
.nav-title {
  font-size: 1.23em;
  font-weight: bold;
  color: #409EFF;
  margin-left:5px;
  letter-spacing: 2px;
  text-shadow: 0 1px 10px #409EFF22;
}
.header-user {
  display: flex;
  align-items: center;
  gap: 4px;
}
.main-area {
  background: linear-gradient(110deg,#f5f6fa 80%, #409EFF11 100%);
  min-height: calc(100vh - 62px);
  padding: 42px 30px 32px 30px;
  transition: background 0.3s;
  border-radius: 12px;
  box-shadow: 0 6px 32px #409EFF11;
}
</style>