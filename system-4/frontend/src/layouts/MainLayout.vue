<template>
  <el-container style="height: 100vh;">
    <el-aside width="212px" class="sidebar">
      <div class="logo-bar">
        <!-- 新logo SVG图标 -->
        <svg class="logo-img" width="38" height="38" viewBox="0 0 1024 1024">
          <circle cx="512" cy="512" r="500" fill="#fffbe6"/>
          <path d="M220 700l84-363 208 278 208-278 84 363z" fill="#FFD700"/>
          <circle cx="220" cy="337" r="50" fill="#FFD700"/>
          <circle cx="512" cy="180" r="60" fill="#FFD700"/>
          <circle cx="804" cy="337" r="50" fill="#FFD700"/>
        </svg>
        <span>授权管理系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="var(--menu-bg)"
        text-color="var(--menu-text)"
        active-text-color="var(--menu-active)"
        style="border-right:none;flex:1 1 auto;"
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
      </el-menu>
      <div class="sidebar-bottom">
        <el-select v-model="themeVal" @change="toggleTheme" style="width:100px; margin-bottom:16px;">
          <el-option label="亮色" value="light" />
          <el-option label="夜间" value="dark" />
          <el-option label="极简" value="minimal" />
          <el-option label="炫彩" value="colorful" />
        </el-select>
        <el-button class="logout-btn" type="danger" plain @click="logout" style="width:100%;">
          <el-icon style="vertical-align:-2px;"><SwitchButton /></el-icon>
          <span style="margin-left:6px;">退出登录</span>
        </el-button>
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
          <el-avatar size="default" style="background:#409EFF;">A</el-avatar>
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
  height: 100vh;
  /* 让底部按钮区固定在底部 */
  position: relative;
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
  color: var(--menu-text);
  text-shadow: 0 2px 16px #409EFF50;
  user-select: none;
}
.logo-img {
  height: 38px;
  margin-right: 7px;
}
.sidebar-bottom {
  width: 100%;
  position: absolute;
  left: 0;
  bottom: 0;
  padding: 18px 0 18px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--menu-bg);
  /* 可选：加点阴影分隔感 */
  box-shadow: 0 -2px 14px #409EFF11;
}
.logout-btn {
  margin-top: 0;
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
/* 极简模式无圆角 */
[data-theme="minimal"] .sidebar,
[data-theme="minimal"] .logo-bar,
[data-theme="minimal"] .main-area,
[data-theme="minimal"] .header-bar,
[data-theme="minimal"] .el-menu,
[data-theme="minimal"] .el-menu-item,
[data-theme="minimal"] .el-menu-item.is-active,
[data-theme="minimal"] .el-card,
[data-theme="minimal"] .el-table,
[data-theme="minimal"] .el-form,
[data-theme="minimal"] .el-input,
[data-theme="minimal"] .el-input__inner,
[data-theme="minimal"] .el-button {
  border-radius: unset !important;
  background: unset !important;
  box-shadow: unset !important;
  border: unset !important;
  margin: unset !important;
}
</style>