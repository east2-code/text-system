<template>
  <div v-if="isLoginPage">
    <router-view />
  </div>
  <el-container v-else style="height:100vh;">
    <el-aside width="220px" class="side-bar">
      <div class="side-title">
        <el-icon><UserFilled /></el-icon>
        <span>{{ $t('loginTitle') }}</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        router
        background-color="var(--aside-bg)"
        text-color="var(--aside-color)"
        active-text-color="var(--aside-active)"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>{{ $t('dashboard') }}</span>
        </el-menu-item>
        <el-menu-item index="/licenses">
          <el-icon><Tickets /></el-icon>
          <span>{{ $t('licenseManage') }}</span>
        </el-menu-item>
        <el-menu-item index="/software">
          <el-icon><Cpu /></el-icon>
          <span>{{ $t('softwareManage') }}</span>
        </el-menu-item>
        <el-menu-item index="/logs">
          <el-icon><Document /></el-icon>
          <span>{{ $t('operationLog') }}</span>
        </el-menu-item>
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>{{ $t('settings') }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="top-bar">
        <span class="top-title">{{ $t('loginTitle') }}</span>
        <div style="flex:1"></div>
        <el-dropdown @command="logout">
          <span class="user-dropdown">
            <el-icon><UserFilled /></el-icon>
            <b>admin</b>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">{{ $t('logout') }}</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main class="main-bg">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { HomeFilled, Tickets, Cpu, Document, Setting, UserFilled, ArrowDown } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const isLoginPage = computed(() => route.path === '/login')
const activeMenu = computed(() => {
  if (route.path.startsWith('/licenses')) return '/licenses'
  if (route.path.startsWith('/software')) return '/software'
  if (route.path.startsWith('/logs')) return '/logs'
  if (route.path.startsWith('/settings')) return '/settings'
  return route.path
})
const logout = (cmd) => {
  if (cmd === 'logout') {
    localStorage.removeItem('token')
    window.location.href = '/login'
  }
}
</script>
<style scoped>
:root,
body[data-theme='colorful'] {
  --aside-bg: linear-gradient(160deg,#2053a2 0%,#6ee0ff 100%);
  --aside-color: #fff;
  --aside-active: #ffd04b;
  --aside-hover: #47caff88;
  --main-bg: linear-gradient(90deg,#dbeafe 0,#faffff 100%);
  --top-bar-bg: linear-gradient(90deg,#4fc3f7 0%,#b388ff 100%);
  --font-main: #1a1a1a;
  --font-side: #fff;
  --card-bg: #fff;
  --card-shadow: 0 2px 18px #72cfff22;
  --card-hover: #e3f0ff;
}
body[data-theme='dark'] {
  --aside-bg: #181a29;
  --aside-color: #bbb;
  --aside-active: #ffd04b;
  --aside-hover: #232347;
  --main-bg: #14151a;
  --top-bar-bg: #23232c;
  --font-main: #e9edee;
  --font-side: #fff;
  --card-bg: #24243c;
  --card-shadow: 0 2px 18px #1118;
  --card-hover: #20202a;
}
body[data-theme='light'] {
  --aside-bg: #f5f6f8;
  --aside-color: #555;
  --aside-active: #409EFF;
  --aside-hover: #e3f0ff;
  --main-bg: #f8fafd;
  --top-bar-bg: #fff;
  --font-main: #111;
  --font-side: #409EFF;
  --card-bg: #fff;
  --card-shadow: 0 2px 12px #409eff16;
  --card-hover: #f2f7fa;
}
body[data-theme='minimal'] {
  --aside-bg: #fff;
  --aside-color: #bbb;
  --aside-active: #409EFF;
  --aside-hover: #f6f6f6;
  --main-bg: #fff;
  --top-bar-bg: #fff;
  --font-main: #111;
  --font-side: #555;
  --card-bg: #fff;
  --card-shadow: 0 0 0 #0000;
  --card-hover: #fafbfc;
}
.side-bar {
  background: var(--aside-bg);
  color: var(--aside-color);
  min-height: 100vh;
  box-shadow: 2px 0 12px #0003;
  transition: background 0.5s;
}
.side-title {
  font-size: 22px;
  font-weight: bold;
  padding: 30px 0 24px 24px;
  color: var(--aside-active);
  display: flex;
  align-items: center;
  gap: 10px;
  user-select: none;
  letter-spacing: 2px;
  text-shadow: 0 4px 24px #409EFF77;
}
.el-menu-vertical-demo .el-menu-item {
  transition: background 0.2s, color 0.2s;
}
.el-menu-vertical-demo .el-menu-item:hover {
  background: var(--aside-hover) !important;
  color: var(--aside-active) !important;
  border-radius: 8px;
}
.top-bar {
  display: flex;
  align-items: center;
  background: var(--top-bar-bg);
  border-bottom: 1px solid #eee;
  height: 62px;
  transition: background 0.5s;
}
.top-title {
  font-weight: bold;
  font-size: 22px;
  margin-left: 8px;
  color: var(--font-main);
  letter-spacing: 1.5px;
  text-shadow: 0 2px 12px #fff3;
}
.user-dropdown {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--aside-active);
}
.main-bg {
  background: var(--main-bg);
  min-height: calc(100vh - 62px);
  padding: 30px 38px 0 38px;
  color: var(--font-main);
  transition: background 0.5s, color 0.3s;
}
</style>