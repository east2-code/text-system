# 授权管理系统前端 项目结构说明

本目录为授权管理系统的前端项目，使用 Vue3 + Vite + Element Plus + axios 实现。  
本说明文档介绍每个主要文件/文件夹的作用，便于理解和维护。

---

## 根目录文件/文件夹

- `.env`  
  环境变量文件，配置前端请求后端 API 的基础地址（如 `VITE_API_BASE=http://localhost:5000/api`）。

- `package.json`  
  项目依赖说明和常用脚本（开发、打包等）。

- `vite.config.js`  
  Vite 构建工具的配置，包含本地开发服务器的代理设置等。

- `README.md`  
  使用说明文档（本文件）。

- `public/`  
  公共资源目录，内容会原样拷贝到打包后的根目录。通常放 favicon、图标等。

---

## src/ 目录（主要源代码）

- `src/main.js`  
  项目入口文件。初始化 Vue 应用，加载 Element Plus UI 框架和路由。

- `src/App.vue`  
  根组件，所有页面内容都由 `<router-view />` 动态渲染。

- `src/api/index.js`  
  axios 实例封装，统一处理所有后端 API 请求，自动携带 token，统一错误提示。

- `src/router/index.js`  
  前端路由配置。定义各个页面的访问路径，并设置登录权限控制。

- `src/assets/`  
  静态资源目录（如图片、LOGO等），可按需添加。

- `src/components/`  
  可复用的小组件目录，目前为空，后续可扩展（如表格、弹窗等通用组件）。

- `src/views/`  
  所有页面主组件目录：

  - `Dashboard.vue`  
    仪表盘首页。显示欢迎信息及授权统计数据。

  - `Login.vue`  
    登录页面。输入用户名、密码，调用后端 `/api/login` 完成登录。

  - `LicenseList.vue`  
    授权列表页。展示所有授权信息，可新增授权、删除授权、查看详情。

  - `LicenseDetail.vue`  
    授权详情页。展示单个授权的详细信息。

  - `SoftwareList.vue`  
    软件管理页。展示所有可授权的软件，支持新增和删除软件。

---

## 其它说明

- 所有页面均基于 Element Plus 组件库开发，样式美观，交互友好。
- 登录后自动保存 token 到本地存储，API 请求自动携带。
- API 路径统一在 `.env` 文件中配置，便于对接不同后端环境。
- 支持直接 `npm run dev` 启动开发环境，`npm run build` 打包发布。

---

如需扩展功能（如权限管理、操作日志、国际化等），可在现有结构基础上增加页面或组件。

---