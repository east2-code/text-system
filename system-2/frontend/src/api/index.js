import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000,
})

instance.interceptors.request.use(config => {
  // 可加 token
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = 'Bearer ' + token
  return config
})

instance.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response && err.response.data) return Promise.reject(err.response.data)
    return Promise.reject({ error: err.message })
  }
)

export default {
  get: (url, params) => instance.get(url, { params }),
  post: (url, data) => instance.post(url, data),
  patch: (url, data) => instance.patch(url, data),
  delete: url => instance.delete(url)
}