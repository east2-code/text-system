<template>
  <el-card style="max-width:480px;margin:0 auto;">
    <h2>{{ $t('settings') }}</h2>
    <el-form label-width="110px">
      <el-form-item :label="$t('language')">
        <el-radio-group v-model="lang" @change="changeLang">
          <el-radio label="zh">{{ $t('zhCN') }}</el-radio>
          <el-radio label="en">{{ $t('enUS') }}</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item :label="$t('theme')">
        <el-radio-group v-model="theme" @change="changeTheme">
          <el-radio label="colorful">🌈 {{ $t('colorful') }}</el-radio>
          <el-radio label="dark">🌙 {{ $t('dark') }}</el-radio>
          <el-radio label="light">☀️ {{ $t('light') }}</el-radio>
          <el-radio label="minimal">🪶 {{ $t('minimalMode') }}</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
    <div v-if="theme==='colorful'" class="theme-tip colorful-tip">
      {{ $t('colorfulTip') }}
    </div>
    <div v-if="theme==='dark'" class="theme-tip dark-tip">
      {{ $t('darkTip') }}
    </div>
    <div v-if="theme==='light'" class="theme-tip light-tip">
      {{ $t('lightTip') }}
    </div>
    <div v-if="theme==='minimal'" class="theme-tip minimal-tip">
      {{ $t('minimalTip') }}
    </div>
  </el-card>
</template>
<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()
const lang = ref(locale.value)
const theme = ref(localStorage.getItem('theme') || 'colorful')
const changeLang = (val) => {
  locale.value = val
  localStorage.setItem('locale', val)
  window.location.reload()
}
const changeTheme = (val) => {
  theme.value = val
  document.body.setAttribute('data-theme', val)
  localStorage.setItem('theme', val)
}
</script>
<style scoped>
.theme-tip { margin-top:16px;font-weight:bold;font-size:1.08em; }
.colorful-tip { color: #49f; }
.dark-tip { color: #ffd04b; }
.light-tip { color: #409EFF; }
.minimal-tip { color: #666; }
</style>