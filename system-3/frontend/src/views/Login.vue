<template>
  <div class="login-bg">
    <div class="login-glass">
      <div class="login-header">
        <el-icon size="46"><UserFilled /></el-icon>
        <span>授权管理系统</span>
      </div>
      <el-form @submit.prevent="onLogin" :model="form" label-width="80px" :rules="rules" ref="formRef" class="login-form">
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            autocomplete="username"
            ref="usernameRef"
            @keyup.enter="focusPassword"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="form.password"
            autocomplete="current-password"
            ref="passwordRef"
            @keyup.enter="onLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onLogin" style="width:100%">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="login-footer">
      <span>© 2025 授权管理系统</span>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'
import { UserFilled } from '@element-plus/icons-vue'

const router = useRouter()
const form = reactive({ username: '', password: '' })
const formRef = ref(null)
const usernameRef = ref(null)
const passwordRef = ref(null)
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}
const focusPassword = () => {
  nextTick(() => passwordRef.value.focus())
}
const onLogin = () => {
  formRef.value.validate(async valid => {
    if (!valid) return
    const res = await api.post('/login', form)
    if (res.code === 0 && res.token) {
      localStorage.setItem('token', res.token)
      router.push('/')
    } else {
      ElMessage.error(res.error || '登录失败')
    }
  })
}
</script>
<style scoped>
.login-bg {
  min-height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #050505 0%, #409EFF 100%), url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1050&q=80');
  background-repeat: no-repeat;
  background-size: cover, cover;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}
.login-glass {
  margin-top: -20vh;
  min-width: 370px;
  background: rgba(255,255,255,0.07);
  border-radius: 22px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  backdrop-filter: blur(9px) saturate(180%);
  border: 1px solid rgba(255,255,255,0.18);
  padding: 38px 36px 32px 36px;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: loginAppear 1.2s cubic-bezier(.77,0,.18,1) 0s 1;
}
@keyframes loginAppear {
  from { opacity: 0; transform: translateY(-65px) scale(.96);}
  to   { opacity: 1; transform: translateY(0) scale(1);}
}
.login-header {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2em;
  font-weight: bold;
  color: #fff;
  margin-bottom: 28px;
  gap: 13px;
  text-shadow: 0 4px 24px #409EFF77;
  letter-spacing: 2px;
}
.login-form {
  width: 320px;
}
.login-footer {
  position: absolute;
  bottom: 4vh;
  width: 100vw;
  text-align: center;
  color: #fff;
  opacity: 0.7;
  font-size: 1.1em;
  letter-spacing: 1.5px;
  text-shadow: 0 2px 10px #409EFF;
  user-select: none;
}
/* 只加粗并金色标签，不影响输入内容 */
.login-form :deep(.el-form-item__label) {
  color: #FFD700;
  font-weight: bold;
}
</style>