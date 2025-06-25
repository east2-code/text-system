import { ref, watchEffect } from 'vue'

export const theme = ref(localStorage.getItem('theme') || 'light')

watchEffect(() => {
  document.documentElement.setAttribute('data-theme', theme.value)
  localStorage.setItem('theme', theme.value)
})