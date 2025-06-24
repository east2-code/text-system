# 授权管理系统前端（Vue3）

本前端为授权管理系统的管理后台，基于 Vue3 + Vite + Element Plus + axios 实现，配合 Flask 后端 API 使用。

## 目录说明

- `src/api/`           —— axios接口封装
- `src/views/`         —— 主要页面（登录、仪表盘、授权、软件管理等）
- `src/router/`        —— 路由配置
- `src/App.vue`        —— 根组件
- `src/main.js`        —— 入口
- `.env`               —— API地址配置
- `vite.config.js`     —— 代理与构建配置

## 本地开发

```bash
cd frontend
npm install
npm run dev
```

## 对接后端

- 后端API地址在 `.env` 里配置
- 支持本地跨域和生产环境部署

## 打包发布

```bash
npm run build
```
生成的`dist/`目录可用 nginx 或其他静态服务器部署。

---